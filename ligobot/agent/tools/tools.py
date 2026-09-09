import json
from .registry import register
from datetime import datetime
from config import BASE_DIR
import subprocess
from subprocess import CompletedProcess
from pathlib import Path

cwd = str(BASE_DIR)  # Home dir


@register(
    desc="""Returns the system’s current local date and time along with the associated timezone name. The tool uses the system timezone to produce a timezone-aware timestamp, making it suitable for applications that need reliable local time and timezone information.
"""
)
def _get_system_time():
    # Get local time with system timezone details attached
    aware_local = datetime.now().astimezone()

    res = {
        "timezone_aware_local_time": f"{aware_local}",
        "timezone_name": aware_local.tzname(),
    }

    return json.dumps(res)


@register(
    desc="""Execute a shell command and return its standard output, error output, exit code, and the arguments passed to the process.
Use this tool when you need to execute a command on the local system. Do not use it for prohibited commands such as `rm`, `shutdown`, `sudo`, or `reboot`.
The command must be provided as separate arguments rather than as a single command string.
""",
    properties={
        "cmd": {"type": "array", "items": {"type": "string"}},
        "is_shell": {"type": "boolean", "default": False},
    },
    required=["cmd"],
)
def _run_cmd(cmd: list[str], is_shell: bool = False):
    prohibited_cmds = ["rm", "shutdown", "sudo", "reboot", "rmdir"]
    is_cmd_prohibited = any(arg in prohibited_cmds for arg in cmd)

    if is_cmd_prohibited:
        return f"Prohibited command found in command execution: {cmd}"

    shell_response: CompletedProcess = subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True, timeout=10
    )

    output = {
        "cmd_output": shell_response.stdout,
        "diagnostics": shell_response.stderr,
        "error_code": shell_response.returncode,
        "args_passed": cmd,
    }

    return json.dumps(output)


@register(
    desc="""Write data to a file at the specified path.

Use this tool to create a new file or overwrite an existing file.
The `file_path` must be the target file path, and `data` is the content
to write to the file. If `data` is omitted, the file will be empty.

This operation overwrites the existing file contents.""",
    properties={
        "file_path": {"type": "string"},
        "data": {"type": "string", "default": ""},
    },
    required=["file_path"],
)
def _write_file(file_path: str, data=""):
    with open(file=file_path, mode="w", encoding="utf-8") as file:
        file.write(data)

    return f"File '{file_path}' created or overwritten successfully."


@register(
    desc="""Update persistent memory in MEMORY.md.

Use when the user explicitly asks to remember, update, or forget
information that is useful across future conversations.

Before updating, check existing memory and:
- Add genuinely new information.
- Update existing information instead of creating duplicates.
- Remove or correct information the user retracts.
- Do not store temporary, sensitive, unverified, or irrelevant information.""",
    properties={
        "data": {"type": "string"},
    },
    required=["data"],
)
def _update_memory(data: str):
    path = Path(__file__).parents[1] / "template/workspace/MEMORY.md"
    with open(path, "w", encoding="utf-8") as file:
        file.write(data)


@register(desc="""Read the current persistent memory from MEMORY.md.

Use this tool before updating memory to check existing information,
avoid duplicates, and identify any existing information that needs
to be updated or removed.""")
def _read_memory():
    path = Path(__file__).parents[1] / "template/workspace/MEMORY.md"
    return path.read_text(encoding="utf-8")
