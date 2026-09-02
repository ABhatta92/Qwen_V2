# app/config.py

from __future__ import annotations

from pathlib import Path


# ---------------------------------------------------------------------------
# Workspace
# ---------------------------------------------------------------------------
# GCP equivalent: store workspaces in Cloud Storage under a fixed per-session
# prefix. Grant the runtime service account only the bucket permissions it needs.

DEFAULT_WORKSPACE = Path(__file__).resolve().parents[1] / "workspace"

WORKSPACE_ROOT = DEFAULT_WORKSPACE.resolve()


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------
# GCP equivalent: replace these local Ollama settings with a Vertex AI Gemini
# model ID. Use Application Default Credentials from the deployed service account.

QWEN_MODEL = "qwen3:latest"

OLLAMA_API_BASE = "http://localhost:11434"

QWEN_TEMPERATURE = 0.2


# ---------------------------------------------------------------------------
# Command execution
# ---------------------------------------------------------------------------
# GCP equivalent: use an allowlisted Cloud Run Job or Agent Engine code-execution
# environment; do not execute arbitrary shell commands in the agent process.

DEFAULT_COMMAND_TIMEOUT = 120
