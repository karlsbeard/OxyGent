import textwrap

import pytest

from oxygent.oxy.skills import SkillRegistry


def _write_skill(path, *, name: str, description: str, body: str = "# Body"):
    path.mkdir(parents=True, exist_ok=True)
    (path / "SKILL.md").write_text(
        textwrap.dedent(
            f"""\
            ---
            name: {name}
            description: {description}
            resources:
              - references/
            ---

            {body}
            """
        ),
        encoding="utf-8",
    )


def test_discover_ignores_non_skill_subdirs(tmp_path):
    skill_dir = tmp_path / "skills"
    _write_skill(skill_dir / "demo-skill", name="demo-skill", description="d")

    # These must not be treated as independent skills.
    (skill_dir / "demo-skill" / "scripts").mkdir(parents=True)
    (skill_dir / "demo-skill" / "scripts" / "SKILL.md").write_text(
        "---\nname: should-not-load\ndescription: x\n---\n\n# x\n",
        encoding="utf-8",
    )
    (skill_dir / "demo-skill" / "references").mkdir(parents=True)
    (skill_dir / "demo-skill" / "references" / "SKILL.md").write_text(
        "---\nname: should-not-load2\ndescription: y\n---\n\n# y\n",
        encoding="utf-8",
    )

    reg = SkillRegistry(skill_dirs=[str(skill_dir)], auto_discover=True)
    assert reg.has_skill("demo-skill")
    assert not reg.has_skill("should-not-load")
    assert not reg.has_skill("should-not-load2")


def test_discover_precedence_later_overrides_earlier(tmp_path):
    d1 = tmp_path / "skills1"
    d2 = tmp_path / "skills2"
    _write_skill(d1 / "s", name="dup", description="from-1")
    _write_skill(d2 / "s", name="dup", description="from-2")

    reg = SkillRegistry(skill_dirs=[str(d1), str(d2)], auto_discover=True)
    assert reg.get_skill("dup").description == "from-2"


def test_discover_requires_valid_frontmatter(tmp_path):
    d = tmp_path / "skills"
    d.mkdir()
    (d / "bad1").mkdir()
    (d / "bad1" / "SKILL.md").write_text("# missing frontmatter\n", encoding="utf-8")
    (d / "bad2").mkdir()
    (d / "bad2" / "SKILL.md").write_text(
        "---\ndescription: x\n---\n\n# missing name\n",
        encoding="utf-8",
    )

    reg = SkillRegistry(skill_dirs=[str(d)], auto_discover=True)
    assert len(reg) == 0


def test_load_full_content_directory_resources_limited(tmp_path):
    d = tmp_path / "skills"
    skill_path = d / "demo"
    _write_skill(skill_path, name="demo", description="d", body="Use $ARGUMENTS")

    refs = skill_path / "references"
    refs.mkdir(parents=True, exist_ok=True)
    for i in range(60):
        (refs / f"f{i}.txt").write_text(f"file-{i}\n", encoding="utf-8")

    reg = SkillRegistry(skill_dirs=[str(d)], auto_discover=True)
    content = reg.load_full_content("demo")
    assert content is not None
    assert len(content.resources) <= 50
    # Ensure keys are relative paths
    assert all(k.startswith("references/") for k in content.resources.keys())
