"""Workspace tools for the local Qwen agent.

GCP equivalent: use Cloud Storage objects under a per-session prefix and the
runtime service account. Never let model input select an unrestricted bucket.
"""

from __future__ import annotations

from app.config import WORKSPACE_ROOT


MAX_READ_BYTES = 2_000_000
MAX_WRITE_BYTES = 2_000_000


def _resolve(path: str):
    """Resolve a model-supplied path and keep it inside the workspace.

    GCP equivalent: validate the relative object name before joining it to the
    fixed Cloud Storage session prefix.
    """
    candidate = (WORKSPACE_ROOT / path).resolve()

    if candidate != WORKSPACE_ROOT and WORKSPACE_ROOT not in candidate.parents:
        raise ValueError("Path must stay inside the workspace.")

    return candidate


def list_workspace() -> str:
    """List files and directories in the workspace.

    USE THIS TOOL when you need to discover what files exist
    or understand the workspace structure.
    """
    # GCP equivalent: ``storage.Client().list_blobs(bucket, prefix=...)``.
    WORKSPACE_ROOT.mkdir(parents=True, exist_ok=True)

    entries = []

    for path in sorted(WORKSPACE_ROOT.rglob("*")):
        relative = path.relative_to(WORKSPACE_ROOT)
        entries.append(
            f"{relative}{'/' if path.is_dir() else ''}"
        )

    return "\n".join(entries) if entries else "Workspace is empty."


def read_file(path: str) -> str:
    """Read the contents of an existing text file.

    USE THIS TOOL when you need to inspect a specific file.
    """
    # GCP equivalent: download the validated object after enforcing a size
    # limit with Cloud Storage object metadata.
    file_path = _resolve(path)

    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    if file_path.stat().st_size > MAX_READ_BYTES:
        raise ValueError(
            f"File is larger than {MAX_READ_BYTES} bytes."
        )

    return file_path.read_text(encoding="utf-8")


def write_file(path: str, content: str) -> str:
    """Create or overwrite a text file.

    USE THIS TOOL when you need to create, modify, or save a file.

    Examples:
    - Save a Python script -> write_file
    - Save a report -> write_file
    - Modify an existing text file -> write_file

    Do NOT use run_command to create files.
    """
    # GCP equivalent: upload to the validated object with a content type and,
    # when needed, generation preconditions for optimistic concurrency.
    encoded = content.encode("utf-8")

    if len(encoded) > MAX_WRITE_BYTES:
        raise ValueError(
            f"Content is larger than {MAX_WRITE_BYTES} bytes."
        )

    file_path = _resolve(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")

    return f"Wrote {len(encoded)} bytes to {path}."


def search_files(query: str) -> str:
    """Search existing workspace files for text.

    USE THIS TOOL when you need to find where something is defined
    without knowing the file containing it.
    """
    # GCP equivalent: list only the session prefix. For large document sets,
    # index the corpus in Vertex AI Search instead of scanning objects.
    if not query.strip():
        raise ValueError("Search query cannot be empty.")

    WORKSPACE_ROOT.mkdir(parents=True, exist_ok=True)

    matches = []

    for path in WORKSPACE_ROOT.rglob("*"):
        if not path.is_file():
            continue

        try:
            if path.stat().st_size > MAX_READ_BYTES:
                continue

            content = path.read_text(encoding="utf-8")

        except (UnicodeDecodeError, OSError):
            continue

        for line_number, line in enumerate(
            content.splitlines(),
            start=1,
        ):
            if query.lower() in line.lower():
                relative = path.relative_to(WORKSPACE_ROOT)
                matches.append(
                    f"{relative}:{line_number}: {line.strip()}"
                )

    return "\n".join(matches) if matches else "No matches found."
