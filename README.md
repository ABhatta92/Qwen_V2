# Qwen V2 — ADK MVP

Qwen V2 is a deliberately small local agent built with Google's **Agent
Development Kit (ADK)** and **Qwen served by Ollama**.

The purpose of this repository is to establish a clean ADK-native foundation
before adding the philosophy corpus, retrieval, memory, multi-agent workflows,
or Google Cloud deployment.

## Current MVP

```text
                    User
                      |
                      v
                ADK Runtime
                      |
                      v
                 Qwen Agent
                      |
          +-----------+-----------+
          |           |           |
          v           v           v
       list/read    write      run Python
       workspace    files      subprocess
          |           |           |
          +-----------+-----------+
                      |
                      v
                  workspace/
```

The application deliberately has **no custom agent runtime, LLM wrapper, tool
registry, or manual function-calling loop**. Those responsibilities belong to
ADK.

ADK currently supports multiple model providers, including Ollama through its
LiteLLM integration. This repository uses the `ollama_chat/<model>` LiteLLM
provider so the model can remain local during development. See the current ADK
model/provider documentation before changing the integration.

## Requirements

- Python 3.11–3.14
- `uv`
- Ollama
- A Qwen model installed in Ollama

The repository is pinned to Python 3.13 for the development environment.

## Setup

### 1. Install the dependencies

```bash
uv sync
```

### 2. Install and start Ollama

Install Ollama separately, then pull a Qwen model. For example:

```bash
ollama pull qwen3:latest
```

Make sure Ollama is available at:

```text
http://localhost:11434
```

### 3. Configure the local model (optional)

Copy `.env.example` to `.env` if you want to override the defaults:

```bash
cp .env.example .env
```

The defaults are:

```text
OLLAMA_API_BASE=http://localhost:11434
QWEN_MODEL=qwen3:latest
QWEN_TEMPERATURE=0.2
```

## Run the agent

The simplest development path is the ADK web playground:

```bash
uv run adk web
```

Open the local URL printed by ADK (normally `http://localhost:8000` or the
port selected by the CLI), select the `app` agent, and start chatting.

You can also run the agent from the command line using ADK's CLI tooling. The
current Google workflow supports local playground development and hot reload.

## Tools

The MVP exposes four plain Python tools:

| Tool | Purpose |
|---|---|
| `list_workspace` | List the agent's available files and directories |
| `read_file` | Read UTF-8 text from `workspace/` |
| `write_file` | Create or replace UTF-8 text files inside `workspace/` |
| `run_python` | Execute Python in a subprocess with `workspace/` as its working directory |

ADK's tool model is intentionally simple: tools are Python callables and their
docstrings describe the capability to the LLM.

### Workspace boundary

The model supplies logical paths such as:

```text
files/notes.txt
scripts/analyze.py
```

The tools resolve those paths under:

```text
workspace/
```

Path traversal outside the workspace is rejected.

### Python execution

`run_python` is intentionally a **local development MVP**, not a production
sandbox. It runs generated Python in a subprocess with a timeout, but it uses
the host Python environment and inherited environment variables.

Do not treat this as a security boundary. For production deployment, use an
isolated execution environment such as the Google Cloud Agent Runtime sandbox
or another dedicated sandbox. ADK's Agent Runtime code-execution integration
can be used even when the main ADK agent is running locally.

## Project structure

```text
qwen_v2/
├── app/
│   ├── __init__.py
│   ├── agent.py              # ADK root agent + App
│   └── tools/
│       ├── __init__.py
│       └── workspace.py      # Local workspace capabilities
├── tests/
│   └── test_workspace_tools.py
├── workspace/
│   └── .gitkeep
├── .env.example
├── .gitignore
├── agents-cli-manifest.yaml
├── GEMINI.md
├── pyproject.toml
├── README.md
└── uv.lock
```

## Reading this repository

Read the project in this order:

1. **`app/agent.py`** — the ADK `Agent`, model configuration, instruction, tools,
   and `App`.
2. **`app/tools/workspace.py`** — the actual local capabilities and workspace
   boundary.
3. **`tests/test_workspace_tools.py`** — the small deterministic test suite.
4. **`pyproject.toml`** — dependency and project configuration.
5. **`agents-cli-manifest.yaml`** — current Agents CLI project metadata.

The key architectural idea is that ADK owns agent orchestration. We should not
reintroduce the old custom `Agent`, `LLM`, `ToolRegistry`, or provider adapter
layers from the previous implementation.

## Why this is intentionally small

The old project had begun implementing its own miniature agent framework:

```text
Agent
  -> LLM adapter
  -> ToolRegistry
  -> Tool abstraction
  -> manual tool loop
```

The ADK MVP replaces that with:

```text
ADK Agent
  -> model
  -> Python tools
  -> ADK runtime
```

That gives us a clean foundation for the actual project goal without committing
prematurely to a large architecture.

The next layers should be added only when needed:

```text
MVP
 |
 +-- retrieval / vector corpus
 |
 +-- conversation memory
 |
 +-- evaluation
 |
 +-- specialist agents / workflows
 |
 +-- Google Cloud model + infrastructure
```

Do **not** add all of those at once.

## Local → GCP migration

The intended future architecture is:

```text
LOCAL DEVELOPMENT

ADK
 |
 +-- Qwen / Ollama
 +-- local workspace
 +-- local retrieval backend
 +-- local evaluation


GCP DEPLOYMENT

ADK
 |
 +-- Gemini / Vertex AI
 +-- Cloud Storage / managed data
 +-- managed retrieval infrastructure
 +-- Agent Runtime / Cloud Run / GKE
 +-- Cloud Trace / logging
```

ADK is the application-level agent framework in both environments. The model
and infrastructure can change underneath it.

Google's current project tooling uses `app/agent.py`, an ADK `App`, a
`pyproject.toml`, `agents-cli-manifest.yaml`, and an `uv.lock`; this repository
follows that current structure while deliberately using no deployment
infrastructure yet.

## Tests and linting

Run the deterministic tests with:

```bash
uv run pytest
```

Run Ruff with:

```bash
uv run ruff check .
```

## Agents CLI (optional)

Google's current Agents CLI can install ADK-specific development, evaluation,
deployment, and observability skills into supported coding agents. It is not a
runtime dependency of this project.

```bash
uvx google-agents-cli setup --workspace
```

The repository includes `agents-cli-manifest.yaml` so it can be recognized as
an ADK project by the current tooling.

## Current scope

Included:

- ADK 2.x foundation
- Local Qwen through Ollama
- ADK-native tool calling
- Controlled workspace read/write
- Local Python execution
- Local development via ADK
- Basic deterministic tests
- uv dependency configuration (lockfile regeneration note included)
- Repository housekeeping

Not included yet:

- RAG / vector database
- book ingestion / chunking
- long-term memory
- multi-agent workflows
- production sandboxing
- Google Cloud deployment
- UI beyond ADK's development playground

Those are subsequent milestones, not part of the MVP.
