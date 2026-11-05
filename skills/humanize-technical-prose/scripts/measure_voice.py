#!/usr/bin/env python3
"""Measure the author's own prose in named samples, and store the counts as a voice profile.

Counts only. What counts as a slip, and its mechanism or cause, is the skill's judgement; it reaches
this script as a tally of numbers keyed by a fixed vocabulary, and `check_tally` refuses anything else,
so no slipped word can be stored. A favoured phrase is kept only when it recurs (in two samples, or
three times in one) and holds no capitalised word past a sentence's start, so a one-off detail or a
client's name stays out of the file. No stored string is longer than four words.

Usage:
  measure_voice.py --measure <sample paths…>                        print the measures as JSON
  measure_voice.py --draft <file>                                   measure one draft: no floor, no phrases
  measure_voice.py --build <name> --slips <tally.json | -> <sample paths…>   write the profile

The profile lands in $HTP_PROFILE_DIR, or ~/.claude/humanize-technical-prose/profiles/ by default.
Exit 0 on success, 2 on a refusal (a transcript, a bad name, a bad tally), printed as JSON.
"""
import collections
import datetime
import json
import os
import re
import statistics
import sys
from pathlib import Path

EXTENSIONS = {".md": "md", ".markdown": "md", ".txt": "txt", ".tex": "tex"}
MIN_WORDS = 500
NAME = re.compile(r"^[a-z0-9][a-z0-9-]*$")
PLACEHOLDERS = {"CODE", "QUOTE", "N", "URL"}

CONNECTIVES = [
    "on the other hand", "as a result", "in addition", "for example", "for instance", "in fact",
    "of course", "that said", "in other words", "however", "thus", "therefore", "hence", "so", "but",
    "and", "also", "still", "yet", "then", "instead", "moreover", "furthermore", "consequently",
    "finally", "first", "second", "fortunately", "unfortunately", "ultimately", "perhaps", "now",
]
CONTRACTED_S = {"it's", "that's", "there's", "here's", "what's", "who's", "let's", "he's", "she's",
                "where's"}
STOP = {"the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "is", "it", "that", "this", "as",
        "at", "by", "with", "be", "are", "was", "were", "its", "from", "but", "not", "can", "will"}
EDGE_STOP = {"the", "a", "an", "and", "or", "of"}

MISSPELLING_MECHANISMS = {"dropped letter", "added letter", "swapped letters", "wrong vowel",
                          "wrong doubling", "other"}
GRAMMAR_CAUSES = {
    "revision residue": {"doubled word", "stray word", "words out of order"},
    "omission": {"dropped article", "dropped word"},
    "substitution": {"wrong word", "wrong form", "number agreement", "wrong article",
                     "punctuation or case"},
}


# --- the author's own prose ---------------------------------------------------------------------

def _inline(text):
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"`[^`]*`", " CODE ", text)
    text = re.sub(r"https?://\S+", " URL ", text)
    text = re.sub(r"[\"“][^\"”]*[\"”]", " QUOTE ", text)
    return text


def _markdown(text):
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    text = re.sub(r"^(```|~~~).*?^\1[^\n]*$", "", text, flags=re.S | re.M)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    kept = []
    for block in re.split(r"\n\s*\n", text):
        lines = [l for l in block.splitlines() if l.strip()]
        if not lines:
            continue
        first = lines[0].lstrip()
        if re.match(r"(#|\||>|[-*+]\s|\d+[.)]\s)", first) or all(l.startswith(("    ", "\t")) for l in lines):
            continue
        kept.append(" ".join(l.strip() for l in lines))
    return "\n\n".join(_inline(b) for b in kept)


TEX_DROP = ("verbatim", "lstlisting", "minted", "figure", "table", "tabular", "equation", "align",
            "gather", "multline", "eqnarray", "math", "displaymath", "quote", "quotation", "verse",
            "itemize", "enumerate", "description", "thebibliography", "algorithm", "algorithmic")


def _latex(text):
    text = re.sub(r"(?<!\\)%.*", "", text)
    if r"\begin{document}" in text:
        text = text.split(r"\begin{document}", 1)[1]
    for env in TEX_DROP:
        text = re.sub(r"\\begin\{" + env + r"\*?\}.*?\\end\{" + env + r"\*?\}", "\n\n", text, flags=re.S)
    text = re.sub(r"\\\[.*?\\\]|\$\$.*?\$\$", " ", text, flags=re.S)
    text = re.sub(r"\$[^$]*\$", " N ", text)
    text = re.sub(r"``.*?''", " QUOTE ", text, flags=re.S)
    text = re.sub(r"\\(sub)*(section|chapter|paragraph|title|caption)\*?\{[^}]*\}", "\n\n", text)
    text = re.sub(r"\\(cite\w*|ref|eqref|label|url|href|includegraphics|bibliography\w*|addcontentsline|"
                  r"setcounter|addtocounter|setlength|vspace|hspace|input|include|newcommand|"
                  r"renewcommand|pagestyle|thispagestyle|pagenumbering)\*?(\[[^\]]*\])?(\{[^}]*\})+", " ", text)
    text = re.sub(r"\\texttt\{[^}]*\}", " CODE ", text)
    text = re.sub(r"\\(textit|textbf|emph|textsc|underline|footnote)\{", " ", text)
    text = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", text)
    text = re.sub(r"[{}~]", " ", text)
    return text


def own_prose(text, kind):
    """The sample's own prose, with code, quotations, headings, tables, lists and markup removed."""
    if kind == "md":
        text = _markdown(text)
    elif kind == "tex":
        text = _latex(text)
    paragraphs = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", text)]
    return "\n\n".join(p for p in paragraphs if p)


# --- sentences and counts ------------------------------------------------------------------------

ABBREV = re.compile(r"\b(e\.g|i\.e|etc|vs|cf|al|Fig|Figs|Eq|Eqs|Dr|Mr|Ms|No|approx|a\.u)\.", re.I)


def sentences(text):
    protected = ABBREV.sub(lambda m: m.group(0).replace(".", "<DOT>"), text)
    protected = re.sub(r"(\d)\.(\d)", r"\1<DOT>\2", protected)
    parts = re.split(r"(?<=[.?!])[\"')\]]?\s+(?=[A-Z\"(\[])", protected)
    out = []
    for p in parts:
        s = p.replace("<DOT>", ".").strip()
        if len(words(s)) > 2:
            out.append(s)
    return out


def words(text):
    return re.findall(r"[A-Za-z0-9][\w'’-]*", text)


def _rate(n, d, per):
    return round(n / d * per, 2) if d else 0.0


def measure_text(prose):
    sents = []
    for para in prose.split("\n\n"):
        sents.extend(sentences(para))
    lens = sorted(len(words(s)) for s in sents)
    wc = len(words(prose))
    lower = [w.lower().replace("’", "'") for w in words(prose)]
    contractions = sum(1 for w in lower if re.search(r"n't$|'re$|'ve$|'ll$|'d$|'m$", w) or w in CONTRACTED_S)
    first_person = sum(1 for w in words(prose) if w == "I" or w.lower() in {"me", "my", "mine", "we", "us", "our", "ours"})
    names = {t.lower() for s in sents for t in words(s)[1:] if t[0].isupper()}
    openers = collections.Counter(w for w in (words(s)[0].lower() for s in sents if words(s))
                                  if w not in names and w.upper() not in PLACEHOLDERS)
    conn = collections.Counter()
    for s in sents:
        low = s.lower().lstrip("\"'([ ")
        for c in CONNECTIVES:
            if re.match(re.escape(c) + r"\b", low):
                conn[c] += 1
                break
    n = len(sents)
    return {
        "words": wc,
        "sentences": n,
        "sentence_length": {
            "median": statistics.median(lens) if lens else 0,
            "mean": round(statistics.mean(lens), 1) if lens else 0,
            "p10": lens[len(lens) // 10] if lens else 0,
            "p90": lens[len(lens) * 9 // 10] if lens else 0,
        },
        "short_sentences_per_100": _rate(sum(l <= 6 for l in lens), n, 100),
        "questions_per_100": _rate(sum(s.rstrip("\"')").endswith("?") for s in sents), n, 100),
        "contractions_per_1000": _rate(contractions, wc, 1000),
        "first_person_per_1000": _rate(first_person, wc, 1000),
        "openers": {w: _rate(c, n, 100) for w, c in openers.most_common(10)},
        "connectives": {w: _rate(c, n, 100) for w, c in conn.most_common()},
        "_sentences": sents,
    }


def _ngrams(sents):
    counts = collections.Counter()
    for s in sents:
        toks = words(s)
        for n in (2, 3, 4):
            for i in range(len(toks) - n + 1):
                gram = toks[i:i + n]
                low = [t.lower() for t in gram]
                if any(t in PLACEHOLDERS or re.search(r"\d", t) for t in gram):
                    continue
                if any(t[0].isupper() and (i + j) > 0 for j, t in enumerate(gram)):
                    continue
                if all(t in STOP for t in low) or low[0] in EDGE_STOP or low[-1] in EDGE_STOP:
                    continue
                counts[" ".join(low)] += 1
    return counts


def _phrases(per_sample):
    total, seen_in = collections.Counter(), collections.Counter()
    for counts in per_sample:
        total.update(counts)
        seen_in.update(counts.keys())
    kept = {g: c for g, c in total.items()
            if seen_in[g] >= 2 or any(counts.get(g, 0) >= 3 for counts in per_sample)}
    for g in list(kept):
        if any(g != h and f" {g} " in f" {h} " and kept[h] == kept[g] for h in kept):
            del kept[g]
    top = sorted(kept.items(), key=lambda kv: (-kv[1], -len(kv[0].split()), kv[0]))[:30]
    return [{"phrase": g, "count": c, "samples": seen_in[g]} for g, c in top]


# --- samples -------------------------------------------------------------------------------------

def refusal(path):
    p = Path(path)
    if p.suffix == ".jsonl" or ".claude/projects" in p.resolve().as_posix():
        return "a Claude Code transcript; the profile reads only documents the author names"
    if p.is_file() and p.suffix.lower() not in EXTENSIONS:
        return f"not Markdown, plain text or LaTeX ({p.suffix or 'no extension'})"
    if not p.exists():
        return "no such file or directory"
    return None


def files_of(path):
    """A named file, or every prose file under a named directory: either way, one sample."""
    path = Path(path)
    if path.is_dir():
        return sorted(f for f in path.rglob("*") if f.suffix.lower() in EXTENSIONS and f.is_file())
    return [path]


def build_measures(paths, floor=MIN_WORDS, phrases=True):
    samples, thin, prose_all, per_sample = [], [], [], []
    for sample in paths:
        prose = "\n\n".join(own_prose(f.read_text(errors="replace"), EXTENSIONS[f.suffix.lower()])
                            for f in files_of(sample))
        m = measure_text(prose)
        entry = {"path": str(sample), "words": m["words"]}
        if m["words"] < floor:
            thin.append(entry)
            continue
        samples.append(entry)
        prose_all.append(prose)
        per_sample.append(_ngrams(m["_sentences"]))
    measures = measure_text("\n\n".join(prose_all))
    del measures["_sentences"]
    measures["samples"], measures["thin"] = samples, thin
    if phrases:
        measures["phrases"] = _phrases(per_sample)
    return measures


def check_tally(tally):
    """Refuse a slip tally that is not counts under the fixed vocabulary."""
    def count(v, where):
        if not isinstance(v, int) or isinstance(v, bool) or v < 0:
            raise ValueError(f"{where} must be a whole number of zero or more")

    if set(tally) != {"misspelling", "grammar", "on_name_or_term"}:
        raise ValueError("a tally holds misspelling, grammar and on_name_or_term, and nothing else")
    for k, v in tally["misspelling"].items():
        if k not in MISSPELLING_MECHANISMS:
            raise ValueError(f"unknown misspelling mechanism {k!r}")
        count(v, f"misspelling/{k}")
    for cause, kinds in tally["grammar"].items():
        if cause not in GRAMMAR_CAUSES:
            raise ValueError(f"unknown grammar cause {cause!r}")
        for k, v in kinds.items():
            if k not in GRAMMAR_CAUSES[cause]:
                raise ValueError(f"unknown {cause} kind {k!r}")
            count(v, f"grammar/{cause}/{k}")
    count(tally["on_name_or_term"], "on_name_or_term")
    return tally


def profile_dir(env):
    if env.get("HTP_PROFILE_DIR"):
        return Path(env["HTP_PROFILE_DIR"])
    return Path.home() / ".claude" / "humanize-technical-prose" / "profiles"


# --- command line --------------------------------------------------------------------------------

def _refuse(items):
    print(json.dumps({"refused": items}, indent=2))
    return 2


def main(argv):
    if len(argv) >= 2 and argv[0] == "--draft":
        why = refusal(argv[1])
        if why:
            return _refuse([{"path": argv[1], "why": why}])
        m = build_measures([argv[1]], floor=0, phrases=False)
        print(json.dumps(m, indent=2))
        return 0
    if len(argv) >= 2 and argv[0] == "--measure":
        paths = argv[1:]
    elif len(argv) >= 5 and argv[0] == "--build" and argv[2] == "--slips":
        name, tally_src, paths = argv[1], argv[3], argv[4:]
        if not NAME.match(name):
            return _refuse([{"path": name, "why": "a profile name is lowercase letters, digits and hyphens"}])
    else:
        print(__doc__, file=sys.stderr)
        return 2
    refused = [{"path": p, "why": w} for p in paths if (w := refusal(p))]
    if refused:
        return _refuse(refused)
    measures = build_measures(paths)
    if argv[0] == "--measure":
        print(json.dumps(measures, indent=2))
        return 0
    if not measures["samples"]:
        return _refuse([{"path": s["path"], "why": f"only {s['words']} words of own prose"} for s in measures["thin"]])
    try:
        raw = sys.stdin.read() if tally_src == "-" else Path(tally_src).read_text()
        tally = check_tally(json.loads(raw))
    except (ValueError, json.JSONDecodeError) as e:
        return _refuse([{"path": tally_src, "why": f"slip tally: {e}"}])
    out_dir = profile_dir(os.environ)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{name}.json"
    profile = {"name": name, "built": datetime.date.today().isoformat(),
               "samples": measures.pop("samples"), "thin": measures.pop("thin"),
               "measures": measures, "slips": tally}
    path.write_text(json.dumps(profile, indent=2) + "\n")
    print(json.dumps({"path": str(path), "samples": profile["samples"], "thin": profile["thin"],
                      "words": measures["words"]}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
