# Agent Skills Format Discussion (OxyGent)

## Context

Today the OxyGent "skills" system is prompt-injection based.

- Discovery unit: a directory containing `SKILL.md`
- Required: `SKILL.md` with YAML frontmatter (`name`, `description`) + Markdown body
- Optional: additional files under the same directory can be loaded into context only when
  the skill is activated (via the `resources:` frontmatter list)

The question is whether "only supporting SKILL.md" is reasonable, and whether we should
formally support a richer folder layout:

```
skill-name/
├── SKILL.md (required)
└── Bundled Resources (optional)
    ├── scripts/
    ├── references/
    └── assets/
```

## What We Support Today

1. A skill is already a folder (not a single file) in practice: `skill-name/SKILL.md`.
2. Bundled resources are supported, but only via explicit opt-in:
   - Use `resources:` in SKILL frontmatter to load specific files as plain text.
   - There is no automatic loading of entire directories.

## Scripts: Can OxyGent Execute Them?

Not automatically.

- The skill system itself does not execute code.
- Scripts can only be executed if the runtime exposes an execution tool and it is allowed
  by configuration / allowlist.

Examples in this repo:

- `oxygent/preset_tools/shell_tools.py`: can run shell commands (uses `subprocess.run(..., shell=True)`)
- `oxygent/preset_tools/python_tools.py`: can run arbitrary Python via `exec(...)`

These tools are powerful and potentially unsafe in many deployments, so we should NOT
assume they are present or enabled.

## Decision / Conclusion

1. Keeping `SKILL.md` as the single required entrypoint is correct.
   - It enforces progressive disclosure and keeps activation cheap.
   - It keeps the contract simple: "prompt + optional referenced resources".

2. We can adopt the `scripts/`, `references/`, `assets/` directory layout as a convention,
   but not as a runtime requirement.
   - These directories may exist, but they do nothing unless referenced.
   - Only files listed in `resources:` are loaded into context.

3. `scripts/` are only useful when the runtime intentionally provides an execution tool.
   - If the deployment does not allow shell/python execution, scripts are effectively
     for humans (documentation, templates, helper code).
   - Do not build skills that rely on executing scripts unless the MAS explicitly
     includes and permits the required execution tools.

4. If we ever want script execution as a first-class capability, implement it as a
   dedicated Tool with explicit sandboxing and allowlisting (future work), not as an
   implicit behavior of the skill loader.
