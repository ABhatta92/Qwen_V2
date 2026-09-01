"""Command execution tool for the local Qwen agent."""

from __future__ import annotations

import os
import subprocess

from app.config import DEFAULT_COMMAND_TIMEOUT, WORKSPACE_ROOT


MAX_OUTPUT_CHARS = 20_000


def run_command(
    command: str,
    timeout_seconds: int = DEFAULT_COMMAND_TIMEOUT,
) -> str:
    """Run a shell command with the workspace as its working directory.

    Commands execute with the agent workspace as the current directory.
    The model cannot choose a different working directory.
    """

    if not command.strip():
        raise ValueError("command must not be empty.")

    if timeout_seconds < 1 or timeout_seconds > DEFAULT_COMMAND_TIMEOUT:
        raise ValueError(
            f"timeout_seconds must be between 1 and "
            f"{DEFAULT_COMMAND_TIMEOUT}."
        )

    WORKSPACE_ROOT.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()

    try:
        completed = subprocess.run(
            command,
            cwd=WORKSPACE_ROOT,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            env=env,
        )
    except subprocess.TimeoutExpired as exc:
        return _format_result(
            exit_code=None,
            stdout=_decode_output(exc.stdout),
            stderr=_decode_output(exc.stderr),
            timed_out=True,
            timeout_seconds=timeout_seconds,
        )

    return _format_result(
        exit_code=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )


def _decode_output(output: str | bytes | None) -> str:
    if output is None:
        return ""

    if isinstance(output, bytes):
        return output.decode(errors="replace")

    return output


def _format_result(
    *,
    exit_code: int | None,
    stdout: str,
    stderr: str,
    timed_out: bool = False,
    timeout_seconds: int | None = None,
) -> str:
    stdout = _truncate(stdout)
    stderr = _truncate(stderr)

    if timed_out:
        status = f"timed_out_after: {timeout_seconds}s"
    else:
        status = f"exit_code: {exit_code}"

    return (
        f"{status}\n"
        f"stdout:\n{stdout}\n"
        f"stderr:\n{stderr}"
    )


def _truncate(value: str) -> str:
    if len(value) <= MAX_OUTPUT_CHARS:
        return value

    return value[:MAX_OUTPUT_CHARS] + "\n\n[output truncated]"