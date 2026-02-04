import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from oxygent.oxy.skills import SkillRegistry
from oxygent.preset_tools.skill_tools import run_skill_script
from oxygent.schemas import OxyRequest


def _write_skill(tmp_path: Path, name: str = "demo") -> Path:
    skill_dir = tmp_path / name
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        "---\nname: "
        + name
        + "\ndescription: demo\n---\n\n# Demo\n",
        encoding="utf-8",
    )
    scripts_dir = skill_dir / "scripts"
    scripts_dir.mkdir()
    return skill_dir


def _make_request_with_registry(reg: SkillRegistry) -> OxyRequest:
    class _MAS:
        def __init__(self, r):
            self.skill_registry = r

    return OxyRequest(mas=_MAS(reg))


@pytest.mark.asyncio
@patch("subprocess.run")
async def test_run_skill_script_python_success(mock_run, tmp_path: Path):
    skill_dir = _write_skill(tmp_path, "demo")
    script_path = skill_dir / "scripts" / "hello.py"
    script_path.write_text("print('ok')\n", encoding="utf-8")

    reg = SkillRegistry(skill_dirs=[str(tmp_path)], auto_discover=True)
    req = _make_request_with_registry(reg)

    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "line1\nline2\n"
    mock_result.stderr = ""
    mock_run.return_value = mock_result

    out = await run_skill_script(
        req,
        skill_name="demo",
        script_relpath="hello.py",
        args=["--x", "1"],
        timeout=12,
        tail=10,
    )
    assert out == "line1\nline2"

    called_cmd = mock_run.call_args.args[0]
    assert called_cmd[:2] == [sys.executable, str(script_path.resolve())]
    assert called_cmd[2:] == ["--x", "1"]
    assert mock_run.call_args.kwargs["cwd"] == str(skill_dir)
    assert mock_run.call_args.kwargs["timeout"] == 12


@pytest.mark.asyncio
@patch("subprocess.run")
async def test_run_skill_script_strips_scripts_prefix(mock_run, tmp_path: Path):
    skill_dir = _write_skill(tmp_path, "demo")
    script_path = skill_dir / "scripts" / "hello.py"
    script_path.write_text("print('ok')\n", encoding="utf-8")

    reg = SkillRegistry(skill_dirs=[str(tmp_path)], auto_discover=True)
    req = _make_request_with_registry(reg)

    mock_result = MagicMock(returncode=0, stdout="ok\n", stderr="")
    mock_run.return_value = mock_result

    out = await run_skill_script(
        req,
        skill_name="demo",
        script_relpath="scripts/hello.py",
        args=[],
    )
    assert out == "ok"
    called_cmd = mock_run.call_args.args[0]
    assert called_cmd[1] == str(script_path.resolve())


@pytest.mark.asyncio
@patch("subprocess.run")
async def test_run_skill_script_rejects_escape(mock_run, tmp_path: Path):
    _write_skill(tmp_path, "demo")
    reg = SkillRegistry(skill_dirs=[str(tmp_path)], auto_discover=True)
    req = _make_request_with_registry(reg)

    out = await run_skill_script(
        req,
        skill_name="demo",
        script_relpath="../evil.py",
        args=[],
    )
    assert "inside the skill's scripts" in out
    mock_run.assert_not_called()


@pytest.mark.asyncio
@patch("subprocess.run")
async def test_run_skill_script_unsupported_extension(mock_run, tmp_path: Path):
    skill_dir = _write_skill(tmp_path, "demo")
    (skill_dir / "scripts" / "a.txt").write_text("nope\n", encoding="utf-8")
    reg = SkillRegistry(skill_dirs=[str(tmp_path)], auto_discover=True)
    req = _make_request_with_registry(reg)

    out = await run_skill_script(
        req,
        skill_name="demo",
        script_relpath="a.txt",
        args=[],
    )
    assert "unsupported script type" in out
    mock_run.assert_not_called()
