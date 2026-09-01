"""Root ADK agent for the local Qwen V2 MVP."""

from __future__ import annotations

from pathlib import Path

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models.lite_llm import LiteLlm

from app.config import (
    OLLAMA_API_BASE,
    QWEN_MODEL,
    QWEN_TEMPERATURE,
)
from app.tools.run_command import run_command
from app.tools.workspace import (
    list_workspace,
    read_file,
    search_files,
    write_file,
)


INSTRUCTIONS_PATH = Path(__file__).parent / "personas" / "developer.txt"
INSTRUCTIONS = INSTRUCTIONS_PATH.read_text(encoding="utf-8")


root_agent = Agent(
    name="qwen_v2",
    model=LiteLlm(
        model=f"ollama_chat/{QWEN_MODEL}",
        api_base=OLLAMA_API_BASE,
        temperature=QWEN_TEMPERATURE,
    ),
    description="A local Qwen software development agent.",
    instruction=INSTRUCTIONS,
    tools=[
        list_workspace,
        read_file,
        write_file,
        run_command,
        search_files,
    ],
)

app = App(
    name="app",
    root_agent=root_agent,
)

__all__ = ["app", "root_agent"]