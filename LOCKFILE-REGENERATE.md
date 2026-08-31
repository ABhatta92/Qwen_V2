# uv.lock

`uv.lock` is intentionally not included in this artifact because the execution
sandbox could not reach PyPI while this project was being rebuilt.

From the repository root, run:

```bash
uv lock
uv sync
```

This will resolve the dependencies declared in `pyproject.toml` and create the
current `uv.lock` for the project.
