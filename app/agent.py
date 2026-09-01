"""Root ADK agent for the local Qwen V2 MVP."""

from __future__ import annotations

import os

from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models.lite_llm import LiteLlm

from app.tools.workspace import list_workspace, read_file, write_file
from app.tools.run_command import run_command

INSTRUCTIONS_PATH = Path(__file__).parent / "personas" / "developer.txt"

INSTRUCTIONS = INSTRUCTIONS_PATH.read_text(encoding="utf-8")

load_dotenv()

MODEL = os.getenv("QWEN_MODEL", "qwen3:latest")
OLLAMA_API_BASE = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
TEMPERATURE = float(os.getenv("QWEN_TEMPERATURE", "0.2"))

root_agent = Agent(
    name="qwen_v2",
    model=LiteLlm(
        model=f"ollama_chat/{MODEL}",
        api_base=OLLAMA_API_BASE,
        temperature=TEMPERATURE,
    ),
    description="A local Qwen agent with a controlled workspace and Python execution.",
    instruction=INSTRUCTIONS,
    tools=[list_workspace, read_file, write_file, run_command],
)

app = App(
    name="app",
    root_agent=root_agent,
)

__all__ = ["app", "root_agent"]
