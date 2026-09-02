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

def inspect_tools(callback_context, llm_request):
    print("\n" + "=" * 80)
    print("TOOLS SENT TO MODEL")
    print("=" * 80)

    if llm_request.config.tools:
        for tool in llm_request.config.tools:
            if tool.function_declarations:
                for fn in tool.function_declarations:
                    print(f"\nNAME: {fn.name}")
                    print(f"DESCRIPTION: {fn.description}")
                    print(f"PARAMETERS: {fn.parameters}")

    print("=" * 80 + "\n")

root_agent = Agent(
    name="qwen_v2",
    model=LiteLlm(
        model=f"openai/{QWEN_MODEL}",
        api_base=f"{OLLAMA_API_BASE}/v1",
        api_key="ollama",
        temperature=QWEN_TEMPERATURE,
        extra_body={
            "think": False,
        },
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
    before_model_callback=inspect_tools,
)

app = App(
    name="app",
    root_agent=root_agent,
)

__all__ = ["app", "root_agent"]