import board_sync


def test_save_note_writes_the_text(tmp_path):
    target = tmp_path / "note.md"
    board_sync.save_note(target, "hello")
    assert target.read_text() == "hello"


def test_describe_labels_passes_every_name_to_the_model():
    seen = {}

    def ask_model(prompt, tools):
        seen["prompt"] = prompt
        return "one family"

    assert board_sync.describe_labels(["bug", "wave: discuss"], ask_model) == "one family"
    assert "bug, wave: discuss" in seen["prompt"]


def test_ledger_context_keeps_only_pinned_lines(tmp_path):
    (tmp_path / ".loop-ledger.md").write_text("pinned: keep tests green\nnote: scratch\n")
    assert board_sync.ledger_context(tmp_path) == ["pinned: keep tests green"]


def test_ledger_context_is_empty_without_a_ledger(tmp_path):
    assert board_sync.ledger_context(tmp_path) == []


def test_write_label_region_replaces_only_the_region(tmp_path):
    claude_md = tmp_path / "CLAUDE.md"
    claude_md.write_text("intro\n<!-- labels -->\nold\n<!-- /labels -->\noutro\n")
    board_sync.write_label_region(claude_md, ["bug"])
    assert claude_md.read_text() == "intro\n<!-- labels -->\n- Label `bug`\n<!-- /labels -->\noutro\n"
