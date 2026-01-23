# OxyGent Agent Skills MVP - Phase 1 & 2 Implementation Plan

Last updated: 2026-01-23

## 0. Scope Of This Document

This plan covers the MVP decision in `pj_memory/mvp.md` focusing on:
- Phase 1: Skill Selector (semantic activation) + manual invocation + audit trail
- Phase 2: Quality/Security hardening (selector tuning + call-time enforcement)

Hard requirement: remove ALL ReActAgent-specific skill logic. Skill support must be
implemented at LocalAgent granularity so all LocalAgents benefit uniformly.

## 0.1 Skill Authoring Spec (Normative For This Repo)

This project follows the Agent Skills format and progressive disclosure principles:

- Concise is key: keep `SKILL.md` body under ~500 lines; move detail into references.
- Set appropriate degrees of freedom:
  - High freedom: text guidance where multiple approaches are valid
  - Medium freedom: pseudo-code or parameterized scripts
  - Low freedom: specific scripts / strict sequences for fragile workflows

Skill directory anatomy:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── scripts/      - executable code (python/bash/etc.)
    ├── references/   - documentation intended to be loaded into context as needed
    └── assets/       - files used in produced output (templates, images, fonts, etc.)
```

What NOT to include in a skill directory:
- README.md / changelog / install guides / auxiliary docs. Keep only what the agent needs.

Reference hygiene:
- Avoid deep nesting; references should be linked directly from `SKILL.md`.
- For reference files > 100 lines, include a small table of contents at the top.

## 1. Current Project Overview (As-Is)

### 1.1 Existing Skills Components

- Registry / progressive disclosure
  - `oxygent/oxy/skills/skill_registry.py`
    - Startup loads metadata only from `SKILL.md` frontmatter
    - Runtime loads full content + resources on-demand via `load_full_content()`
    - Current discovery roots default to:
      - `.oxygent/skills/`
      - `~/.oxygent/skills/`
      - `oxygent/preset_skills/`
    - Current `generate_system_prompt_section()` instructs the model to call `Skill(...)`.
- Skill tool
  - `oxygent/oxy/skills/skill_tool.py`
    - Tool name: `Skill`
    - Loads full content and returns:
      - `output`: context injection string
      - `extra.environment_modifications`: `allowed_tools` / `model` / `timeout`
    - `is_permission_required=False` (important for enforcement design)
- Content / metadata models
  - `oxygent/oxy/skills/skill_metadata.py`: strict required `name` + `description`
  - `oxygent/oxy/skills/skill_content.py`: strict required `name` + `description`, parses `allowed-tools`
- MAS init
  - `oxygent/mas.py` initializes `SkillRegistry` and registers `SkillTool` at startup.

### 1.2 Current Agent Integration

- `oxygent/oxy/agents/react_agent.py` contains custom “skills support”:
  - Injects skill catalog into system prompt
  - Handles SkillTool response + applies env_mods (soft tool restriction)

All other agents (`ChatAgent`, `ParallelAgent`, `WorkflowAgent`) do not have skill
catalog injection nor skill activation logic.

## 2. Target Architecture (To-Be)

### 2.1 Core Principle

Implement skill support at `LocalAgent` level so every LocalAgent gains:
- progressive disclosure compatibility
- semantic activation (Phase 1 via selector)
- manual invocation
- uniform audit trail

ReActAgent must not contain any skill-only code paths. It should remain a pure
ReAct loop implementation.

### 2.2 MVP Activation Strategy (Chosen)

Use Phase 1 “Skill Selector” (pre-execute semantic selection) rather than
requiring all agents to implement a tool-call loop.

High-level flow:
1) Receive user query
2) Detect manual invocation (`/skill-name ...`) and activate directly (user source)
3) Else run Skill Selector:
   - input: user query + skill metadata (name/description)
   - output: selected skill or none (+ reason/confidence)
4) If a skill is selected:
   - load/activate skill via SkillTool (model/selector source)
   - inject instructions/resources into the next LLM call context
   - apply env_mods as runtime constraints (Phase 2: strong enforcement)
5) Run the agent's original execution logic

## 3. Compatibility Specification (Claude Skill Standard Subset)

### 3.1 Directory Layout / Discovery

Add discovery support for standard locations:
- Project: `.claude/skills/<skill>/SKILL.md`
- User: `~/.claude/skills/<skill>/SKILL.md`

Keep backward compatibility:
- Project: `.oxygent/skills/<skill>/SKILL.md`
- User: `~/.oxygent/skills/<skill>/SKILL.md`
- Built-in: `oxygent/preset_skills/<skill>/SKILL.md`

Priority (last wins when names collide):
1) `oxygent/preset_skills/`
2) `~/.oxygent/skills/`
3) `.oxygent/skills/`
4) `~/.claude/skills/`
5) `.claude/skills/`

Rationale: project-specific definitions override everything.

### 3.2 Frontmatter Fields (Phase 1 & 2)

MVP must parse and preserve:
- `name` (required)
- `description` (required)
- `argument-hint` (optional; mainly for future UI)
- `disable-model-invocation` (bool; default false)
- `user-invocable` (bool; default true)
- `allowed-tools` (list|string)
- `model` (string)
- `timeout` (number)
- `resources` (list|string; existing)

Out of scope (parse only, no execution semantics in MVP):
- `context: fork`, `agent`, `hooks`
- preprocessing `!` command injection

### 3.3 Invocation Source Model

Define explicit invocation sources:
- `user`: manual invocation via `/skill-name ...`
- `selector`: chosen by pre-execute selector (semantic)
- `model`: direct Skill tool call from a tool-call loop agent

Enforcement rules:
- `disable-model-invocation: true` must block `selector` and `model` sources
  (allow only `user`).

## 4. Detailed Behavior Specs

### 4.1 Manual Invocation Parsing

Syntax (first token in the query):
- `/skill-name` or `/skill-name <arguments...>`

Rules:
- Only treat as manual invocation if query begins with `/` and the first token matches a discovered skill name.
- `arguments` is the remainder of the line (may be empty).
- Preserve the original query in audit trail.

### 4.2 Skill Selector (Phase 1 Baseline)

Selector interface:
- Run one extra LLM call before agent execution.
- Input:
  - user query
  - skill metadata list (name + description) excluding `disable-model-invocation: true`
- Output: strict JSON

Proposed JSON schema:
```
{
  "selected_skill": "<name>" | null,
  "confidence": 0.0-1.0,
  "reason": "..." 
}
```

Phase 1 behavior:
- If `selected_skill` is null: proceed without skill.
- If non-null and skill exists: activate it.
- Phase 1 can ignore confidence threshold (or use a conservative default like `>= 0.6`).

### 4.3 Skill Activation & Injection

Activation must:
- Load skill instructions/resources via SkillTool (progressive disclosure level 2/3).
- Apply `$ARGUMENTS` substitution behavior:
  - If skill instructions contain `$ARGUMENTS`: replace it with provided arguments
  - Else append `ARGUMENTS: <args>` at end of injected content (if args not empty)

Injection placement:
- Prefer injecting into `additional_prompt` (or system prompt tail) so it is always present for the agent's LLM call.

### 4.4 Tool Restrictions (`allowed-tools`)

MVP semantics (Phase 2 hardening):
- Treat `allowed-tools` as a hard allowlist for non-LLM callee invocations while the skill is active.
- Always allow calling the configured `llm_model` (otherwise the agent can't run).

Implementation target:
- Centralize enforcement in `oxygent/schemas/oxy.py:OxyRequest.call()` based on request context
  (e.g., `oxy_request.shared_data` or `oxy_request.arguments` carrying active skill constraints).

### 4.5 Skill Catalog Injection

Since Phase 1 uses a selector, the main agent LLM does NOT need to be instructed to call `Skill(...)`.

MVP guideline:
- Keep metadata available to the system for selection, but avoid telling the main LLM to invoke skills via the Skill tool.
- If catalog is injected into system prompt for transparency, it should state:
  - "Skills may be activated automatically by the system. Do not invoke the Skill tool unless the user explicitly requests it."

## 5. Phase 1 Task Breakdown (Implementation)

### 5.1 Refactor: Remove ReActAgent Skill Logic

Files:
- `oxygent/oxy/agents/react_agent.py`

Tasks:
- Remove skill-related fields (`enable_skills`, `active_skill`, `skill_allowed_tools`, `pending_skill_*`, etc.).
- Remove `_build_instruction()` override that injects skill catalog.
- Remove any SkillTool response handling and skill env_mod application.

Acceptance:
- ReActAgent continues to function as before for non-skill behavior.
- No skill-specific references remain in `react_agent.py`.

### 5.2 LocalAgent: Add Uniform Skill Support Hooks

Files:
- `oxygent/oxy/agents/local_agent.py`

Tasks:
- Add a pre-execute phase to:
  - detect manual invocation
  - run selector if not manual
  - activate skill if selected
- Add a post-execute cleanup phase (clear any one-shot state on the request).

### 5.3 Skill Selector Implementation

Files (new or existing):
- New module recommended: `oxygent/oxy/skills/skill_selector.py`

Tasks:
- Implement a minimal selector prompt template.
- Implement a pure function that:
  - builds selector messages
  - calls agent.llm_model once
  - parses JSON result safely
  - returns `selected_skill` / reason / confidence

### 5.4 Skill Metadata & Content: Standard Field Support

Files:
- `oxygent/oxy/skills/skill_metadata.py`
- `oxygent/oxy/skills/skill_content.py`

Tasks:
- Extend models to parse and store:
  - `disable-model-invocation` (bool)
  - `user-invocable` (bool)
  - `argument-hint` (string)

Behavior:
- If `name` or `description` missing: treat skill as invalid, skip discovery, and log a warning.

### 5.5 SkillRegistry: Discovery + Priority + Catalog Generation

Files:
- `oxygent/oxy/skills/skill_registry.py`

Tasks:
- Update default directories to include `.claude/skills/` and `~/.claude/skills/`.
- Implement explicit precedence rules (do not rely on accidental overwrite order).
- Update catalog generation to exclude skills with `disable-model-invocation: true`.
- Update catalog content so it does not instruct the main LLM to call `Skill(...)`.

### 5.6 SkillTool: Invocation Source & disable-model-invocation Enforcement

Files:
- `oxygent/oxy/skills/skill_tool.py`

Tasks:
- Extend input schema to accept optional:
  - `arguments` (string)
  - `invocation_source` (enum-like string)
- Apply `$ARGUMENTS` substitution and/or appended `ARGUMENTS: ...`.
- Enforce `disable-model-invocation: true`:
  - allow only when invocation_source == `user`
  - return FAILED/SKIPPED with a clear message otherwise

### 5.7 Audit Trail (Trace/History)

Files:
- `oxygent/schemas/oxy.py` (request/response extra)
- (optional) agent logs

Tasks:
- Add standardized fields in `oxy_request.shared_data` or `oxy_request.arguments`:
  - `active_skill_name`
  - `active_skill_source` (user/selector/model)
  - `active_skill_confidence`
  - `active_skill_reason`
  - `active_skill_path`
  - `active_skill_env_mods`

### 5.8 Tests (Phase 1)

Add unit tests around:
- discovery priority & duplicate resolution
- parsing frontmatter fallbacks
- manual invocation parsing
- disable-model-invocation enforcement paths

## 6. Phase 2 Task Breakdown (Quality & Security)

### 6.1 Selector Tuning

Add:
- confidence thresholding (configurable)
- "cooldown" / anti-spam (avoid repeated activation for adjacent turns)
- candidate trimming:
  - top-N by simple heuristic (keyword overlap) BEFORE LLM selection
  - character budget for metadata injected into selector

### 6.2 Call-Time Enforcement Of allowed-tools

Files:
- `oxygent/schemas/oxy.py:OxyRequest.call()`

Tasks:
- If active skill has `allowed-tools` list:
  - allow calls to llm_model always
  - allow calls only to names in allowed-tools for all other callees
  - produce a deterministic refusal response when blocked

### 6.3 Observability Improvements

- Add logs for:
  - selector decision (skill/none)
  - activation outcome (success/failure)
  - blocked tool calls (if any)
- Ensure logs include `trace_id` and `node_id`.

## 7. Acceptance Criteria

Phase 1:
- Any LocalAgent can activate a skill via selector without becoming a tool-call loop agent.
- Manual invocation `/skill-name args` works across LocalAgents.
- `disable-model-invocation: true` skills cannot be activated by selector.
- ReActAgent contains zero skill-specific code.

Phase 2:
- Selector quality controls (threshold + cooldown) reduce over-triggering.
- `allowed-tools` is enforced at call-time (not only via prompt text).

## 8. Non-Goals (Permanent)

- No plan to implement Phase 3 / “evolve to tool-call loop for all agents”. This repository will not pursue
  the all-agents loop architecture for skills; the chosen approach is selector-based activation.

## 9. Notes / Open Questions (Track Here)

- Should we keep a user-facing skill catalog in the main system prompt, or keep it selector-only?
- How do we choose which model is used for selector calls (same as agent.llm_model vs dedicated fast model)?
- Do we need a stable on-disk evaluation set for selector precision/recall before enabling by default?
