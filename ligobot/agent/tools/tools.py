import json
from .registry import register
from datetime import datetime
from config import BASE_DIR
import subprocess
from subprocess import CompletedProcess

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
"""
)
def _run_cmd(*cmd: list[str], is_shell: bool = False):
    prohibited_cmds = ["rm", "shutdown", "sudo", "reboot", "rmdir"]
    is_cmd_prohibited = any(arg in prohibited_cmds for arg in cmd)

    if is_cmd_prohibited:
        return f"Prohibited command found in command execution: {cmd}"

    shell_response: CompletedProcess = subprocess.run(
        *cmd, cwd=cwd, capture_output=True, text=True, timeout=10
    )

    output = {
        "cmd_output": shell_response.stdout,
        "diagnostics": shell_response.stderr,
        "error_code": shell_response.returncode,
        "args_passed": list(cmd),
    }

    return json.dumps(output)
