import logging
import shlex
import subprocess
from typing import List, Optional

from oxygent.oxy import FunctionHub

logger = logging.getLogger(__name__)
shell_tools = FunctionHub(name="shell_tools")


@shell_tools.tool(description="Run a shell command and return the output or error.")
def run_shell_command(
    command: Optional[str] = None,
    args: Optional[List[str]] = None,
    tail: int = 10,
    base_dir: Optional[str] = None,
) -> str:
    """Runs a shell command and returns the output or error."""

    try:
        if command is None:
            args = args or []
            command = " ".join(shlex.quote(str(a)) for a in args)

        logger.info("Running shell command: %s", command)
        result = subprocess.run(
            command,
            capture_output=True,
            encoding="utf8",
            shell=True,
            text=True,
            cwd=base_dir,
        )
        if result.returncode != 0:
            return f"Error: {result.stderr}"
        return "\n".join(result.stdout.split("\n")[-tail:])
    except Exception as e:
        logger.warning(f"Failed to run shell command: {e}")
        return f"Error: {e}"
