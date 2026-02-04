import logging
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

from pydantic import Field

from oxygent.oxy import FunctionHub
from oxygent.schemas import OxyRequest

logger = logging.getLogger(__name__)


skill_tools = FunctionHub(name="skill_tools")


def _tail_text(text: str, tail: int) -> str:
    if not isinstance(text, str) or tail is None:
        return text
    try:
        t = int(tail)
    except Exception:
        return text
    if t <= 0:
        return text
    return "\n".join(text.splitlines()[-t:])


@skill_tools.tool(
    description=(
        "Run a script bundled under a skill's scripts/ directory, resolving the skill path via SkillRegistry. "
        "Only scripts inside <skill>/scripts are allowed."
    )
)
def run_skill_script(
    oxy_request: OxyRequest,
    skill_name: str = Field(description="Skill name (as discovered by SkillRegistry)"),
    script_relpath: str = Field(
        description=(
            "Path relative to the skill's scripts/ directory (e.g. 'init_skill.py'). "
            "If 'scripts/' prefix is provided, it will be stripped."
        )
    ),
    args: Optional[List[str]] = None,
    timeout: int = 60,
    tail: int = 80,
    env: Optional[dict] = None,
) -> str:
    registry = getattr(getattr(oxy_request, "mas", None), "skill_registry", None)
    if not registry:
        return "Error: Skill registry not initialized"

    if not isinstance(skill_name, str) or not skill_name.strip():
        return "Error: skill_name is required"
    if not isinstance(script_relpath, str) or not script_relpath.strip():
        return "Error: script_relpath is required"

    skill_name = skill_name.strip()
    script_relpath = script_relpath.strip()
    if script_relpath.startswith("scripts/"):
        script_relpath = script_relpath[len("scripts/") :]
    if script_relpath.startswith("./"):
        script_relpath = script_relpath[2:]

    try:
        meta = registry.get_skill(skill_name)
    except Exception as e:
        return f"Error: failed to resolve skill '{skill_name}': {e}"
    if not meta or not getattr(meta, "skill_path", None):
        return f"Error: skill '{skill_name}' not found"

    base_dir = Path(meta.skill_path).parent
    scripts_dir = (base_dir / "scripts").resolve()
    target = (scripts_dir / script_relpath).resolve()

    try:
        if not target.is_relative_to(scripts_dir):
            return "Error: script_relpath must be inside the skill's scripts/ directory"
    except Exception:
        # Fallback for very old Python.
        try:
            if os.path.commonpath([str(scripts_dir), str(target)]) != str(scripts_dir):
                return "Error: script_relpath must be inside the skill's scripts/ directory"
        except Exception:
            return "Error: script_relpath must be inside the skill's scripts/ directory"

    if not target.exists() or not target.is_file():
        return f"Error: script not found: {target}"

    ext = target.suffix.lower()
    if ext == ".py":
        cmd = [sys.executable, str(target)]
    elif ext in {".sh", ".bash"}:
        cmd = ["bash", str(target)]
    elif ext == ".zsh":
        zsh = shutil.which("zsh")
        cmd = [zsh or "bash", str(target)]
    else:
        return f"Error: unsupported script type '{ext}' (allowed: .py/.sh/.zsh)"

    if args is None:
        args = []
    elif not isinstance(args, list):
        # Allow passing a single string for convenience.
        if isinstance(args, str) and args.strip():
            args = shlex.split(args)
        else:
            args = []
    cmd.extend([str(a) for a in args])

    # Common case: skill scripts that take an output directory (e.g. init_skill.py --path ...).
    # If the provided path is relative, interpret it relative to the *process* cwd (project root),
    # not the skill directory, to avoid creating nested folders under the skill itself.
    try:
        if "--path" in args:
            i = args.index("--path")
            if i + 1 < len(args) and isinstance(args[i + 1], str):
                p = args[i + 1]
                if p and not os.path.isabs(p):
                    args[i + 1] = str((Path.cwd() / p).resolve())
                    # Rebuild cmd tail with rewritten args
                    cmd = cmd[: len(cmd) - len(args)] + [str(a) for a in args]
    except Exception:
        pass

    run_env = None
    if env is not None:
        if not isinstance(env, dict):
            return "Error: env must be a dict"
        run_env = os.environ.copy()
        run_env.update({str(k): str(v) for k, v in env.items()})

    try:
        logger.info(
            "Running skill script: %s (skill=%s, cwd=%s)",
            cmd,
            skill_name,
            str(base_dir),
        )
        result = subprocess.run(
            cmd,
            capture_output=True,
            encoding="utf-8",
            text=True,
            cwd=str(base_dir),
            timeout=int(timeout) if timeout else None,
            env=run_env,
        )
        out = (result.stdout or "")
        err = (result.stderr or "")
        combined = out
        if err.strip():
            combined = (out.rstrip("\n") + "\n" + err).strip("\n")

        combined = combined.strip("\n")
        combined = _tail_text(combined, tail)

        if result.returncode != 0:
            return f"Error (exit={result.returncode}): {combined}" if combined else f"Error (exit={result.returncode})"
        return combined
    except subprocess.TimeoutExpired:
        return f"Error: script timed out after {timeout}s"
    except Exception as e:
        logger.warning("Failed to run skill script: %s", e)
        return f"Error: {e}"
