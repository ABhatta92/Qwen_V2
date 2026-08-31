"""Root ADK agent for the local Qwen V2 MVP."""

from __future__ import annotations

import os

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models.lite_llm import LiteLlm

from app.tools.workspace import list_workspace, read_file, run_python, write_file

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
    instruction="""
You are Qwendolyn, a local general-purpose agent.

You have three classes of capabilities:
- Inspect the workspace with list_workspace and read_file.
- Create or modify workspace files with write_file.
- Run Python code with run_python.

The workspace is the agent's working environment. Paths supplied to file tools
are relative to workspace/; never assume access to files outside it.

Use tools when they materially help accomplish the user's request. For Python
work, prefer run_python for computation or scripts and inspect the output before
claiming that something worked.

Be explicit about tool results and failures. Do not claim to have changed a file
or executed code unless the corresponding tool returned successfully.
""",
    tools=[list_workspace, read_file, write_file, run_python],
)

app = App(
    name="app",
    root_agent=root_agent,
)

__all__ = ["app", "root_agent"]
