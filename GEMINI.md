# Qwen V2 development guidance

- This project uses Google ADK as the agent runtime.
- Qwen is served locally by Ollama through ADK's LiteLLM integration.
- Keep agent orchestration in ADK; do not recreate an Agent/Runner/tool registry.
- ADK tools should be plain Python callables with clear docstrings.
- Keep local infrastructure behind small application boundaries so it can later
  be replaced by Google Cloud equivalents.
- Do not add multi-agent orchestration, RAG, memory, or deployment infrastructure
  until the single-agent MVP is working and tested.
- Never put secrets in source control.
