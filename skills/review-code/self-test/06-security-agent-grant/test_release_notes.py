import json

import release_notes


def test_the_reader_is_started_with_its_own_definition():
    argv = release_notes.command("history-reader", "since v1.2")
    assert argv[:3] == ["claude", "-p", "since v1.2"]
    assert json.loads(argv[argv.index("--agents") + 1]) == release_notes.AGENTS
    assert argv[-2:] == ["--agent", "history-reader"]


def test_the_drafter_holds_no_shell():
    assert "Bash" not in " ".join(release_notes.AGENTS["notes-drafter"]["tools"])
