# app/config.py

from __future__ import annotations

from pathlib import Path


# ---------------------------------------------------------------------------
# Workspace
# ---------------------------------------------------------------------------

DEFAULT_WORKSPACE = Path(__file__).resolve().parents[1] / "workspace"

WORKSPACE_ROOT = DEFAULT_WORKSPACE.resolve()


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

QWEN_MODEL = "qwen3:latest"

OLLAMA_API_BASE = "http://localhost:11434"

QWEN_TEMPERATURE = 0.2


# ---------------------------------------------------------------------------
# Command execution
# ---------------------------------------------------------------------------

DEFAULT_COMMAND_TIMEOUT = 120