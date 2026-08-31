from pathlib import Path

from app.tools import workspace


def test_write_and_read(tmp_path, monkeypatch):
    monkeypatch.setattr(workspace, "WORKSPACE_ROOT", tmp_path)

    assert "Wrote" in workspace.write_file("notes/test.txt", "hello")
    assert workspace.read_file("notes/test.txt") == "hello"


def test_path_escape_is_rejected(tmp_path, monkeypatch):
    monkeypatch.setattr(workspace, "WORKSPACE_ROOT", tmp_path)

    try:
        workspace.read_file("../outside.txt")
    except ValueError as exc:
        assert "inside the workspace" in str(exc)
    else:
        raise AssertionError("Path escape was not rejected")


def test_run_python(tmp_path, monkeypatch):
    monkeypatch.setattr(workspace, "WORKSPACE_ROOT", tmp_path)

    result = workspace.run_python("print(2 + 2)")
    assert "exit_code: 0" in result
    assert "4" in result
