"""Workspace tools for the local Qwen agent."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parents[2] / "workspace"
DEFAULT_TIMEOUT_SECONDS = 30
MAX_READ_BYTES = 2_000_000
MAX_WRITE_BYTES = 2_000_000


def _resolve(path: str) -> Path:
    """Resolve a model-supplied path and keep it inside the workspace."""
    candidate = (WORKSPACE_ROOT / path).resolve()
    root = WORKSPACE_ROOT.resolve()
    if candidate != root and root not in candidate.parents:
        raise ValueError("Path must stay inside the workspace.")
    return candidate


def list_workspace() -> str:
    """List files and directories available inside the local workspace."""
    WORKSPACE_ROOT.mkdir(parents=True, exist_ok=True)
    entries = []
    for path in sorted(WORKSPACE_ROOT.rglob("*")):
        relative = path.relative_to(WORKSPACE_ROOT)
        entries.append(f"{relative}{'/' if path.is_dir() else ''}")
    return "\n".join(entries) if entries else "Workspace is empty."


def read_file(path: str) -> str:
    """Read a UTF-8 text file from the workspace. Path is relative to workspace/."""
    file_path = _resolve(path)
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    if file_path.stat().st_size > MAX_READ_BYTES:
        raise ValueError(f"File is larger than {MAX_READ_BYTES} bytes.")
    return file_path.read_text(encoding="utf-8")


def write_file(path: str, content: str) -> str:
    """Write UTF-8 text to a file inside the workspace, creating parent directories."""
    if len(content.encode("utf-8")) > MAX_WRITE_BYTES:
        raise ValueError(f"Content is larger than {MAX_WRITE_BYTES} bytes.")
    file_path = _resolve(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")
    return f"Wrote {len(content.encode('utf-8'))} bytes to {path}."
