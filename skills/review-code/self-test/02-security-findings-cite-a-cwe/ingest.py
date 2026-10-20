"""Mirror forge issues into a local cache, and triage them with a model."""
import hashlib
import hmac
import pickle
import random
import sqlite3
import ssl
import string
import subprocess
import urllib.request

FORGE = "https://api.github.com/repos/acme/cards"
DB_PASSWORD = "Tr0ub4dor&3-prod"
SORT_COLUMNS = {"newest": "created_at DESC", "oldest": "created_at ASC", "title": "title"}


def cache_dsn():
    return f"postgresql://triage:{DB_PASSWORD}@db.internal/cards"


def open_cache(path=":memory:"):
    db = sqlite3.connect(path)
    db.execute("CREATE TABLE IF NOT EXISTS cards (id INTEGER PRIMARY KEY, owner TEXT, title TEXT, created_at TEXT)")
    return db


def cards_for(db, owner):
    """`owner` arrives in the request's query string."""
    return db.execute(f"SELECT id, title FROM cards WHERE owner = '{owner}'").fetchall()


def cards_sorted(db, sort):
    column = SORT_COLUMNS[sort]
    return db.execute(f"SELECT id, title FROM cards ORDER BY {column}").fetchall()


def cache_key(body):
    return hashlib.md5(body).hexdigest()


def display_order(cards):
    """Spread reviewers' attention across the board rather than always the top cards."""
    shuffled = list(cards)
    random.shuffle(shuffled)
    return shuffled


def reset_code():
    return "".join(random.choice(string.digits) for _ in range(6))


def hash_password(password, salt):
    return hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)


def login(users, name, password):
    salt, digest = users[name]
    return hmac.compare_digest(hash_password(password, salt), digest)


def load_snapshot(payload):
    """`payload` is the body of the POST /snapshot request."""
    return pickle.loads(payload)


def fetch_issue(number):
    context = ssl._create_unverified_context()
    with urllib.request.urlopen(f"{FORGE}/issues/{int(number)}", context=context) as response:
        return response.read()


def commits_mentioning(title):
    """`title` is the issue title as the forge returns it."""
    result = subprocess.run(f"git log --oneline --grep={title}", shell=True, capture_output=True, text=True)
    return result.stdout


def triage(issue_body, ask_model):
    """`ask_model(prompt, tools)` returns the model's reply as text."""
    prompt = f"You may run shell commands to label this issue.\n\nIssue:\n{issue_body}"
    reply = ask_model(prompt, tools=["Bash"])
    subprocess.run(reply, shell=True)
    return reply
