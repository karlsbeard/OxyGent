# oxygent 框架支持 skills能力

## 功能需求

参照标准的 Claude Agent Skills / Claude Code skills 规范进行实现，并将方案讨论、阶段规划、取舍与风险留痕归档，便于后续沟通、汇报与回溯。

---

# OxyGent Agent Skills（Skill）能力 - MVP PRD / 方案归档

## 1. 背景与问题陈述

OxyGent 当前已经具备 Skill 基础支持（SkillRegistry + SkillTool + MAS 启动初始化），但存在两个关键缺口：
1) 仅支持 SKILL.md 的“非标准化/不完整规范”（字段/目录约定与业界 open standard、Claude Code 规范存在偏差）
2) Skill 能力仅在 ReActAgent 上生效，其他 Agent（ChatAgent/ParallelAgent/WorkflowAgent 等）缺失“语义触发 + 注入生效”的链路

本 PRD 目标是在不大改现有 agent 架构的前提下，让“所有 LocalAgent 体系”都具备：
- 渐进式披露（progressive disclosure）：metadata 常驻、正文按需加载、资源按需访问
- 语义触发（semantic / model-invoked）：在合适的时候自动触发 Skill
- 显式触发（manual / user-invoked）：用户点名调用 Skill
- 留痕可追溯（trace/history/log）

## 2. 参考规范（归档）

- Claude Code: Extend Claude with skills
  - https://code.claude.com/docs/en/skills
- Claude Agent Skills（概念/渐进式披露）
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- GitHub Copilot Agent Skills（同样强调 progressive disclosure，目录在 .github/skills 与 .claude/skills）
  - https://code.visualstudio.com/docs/copilot/customization/agent-skills

关键规范点（抽取）：
- Skill 为目录结构，入口为 `SKILL.md`，包含 YAML frontmatter + markdown body
- 元信息（name/description）常驻；正文只在触发时加载；其他资源文件按需读取/执行
- `disable-model-invocation: true` 用于禁止模型自动触发（防止部署/提交等有副作用动作被自动执行）
- `allowed-tools` 用于约束 skill 激活时允许调用的工具（Claude Code 中可用；不同平台实现细节不同）

## 3. 设计决策：Skill 能力下沉到 LocalAgent 粒度

### 3.1 为什么是 LocalAgent（而不是 BaseAgent）

Skill 的实际效果依赖于 LocalAgent 的运行时要素：
- system prompt 组装（注入 skills catalog、注入 skill 正文）
- 工具描述与工具可用性（allowed-tools 限制）
- model/timeout 的本次调用 override
- memory/trace 写入留痕

BaseAgent 更偏“抽象生命周期与 trace 存储”，缺少上述 prompt/tools 执行入口；因此：
- 通用技能能力（catalog 注入、语义触发、注入生效、留痕）应落在 LocalAgent
- ReActAgent 继续保留其 loop 特性，但尽量复用 LocalAgent 的通用实现

## 4. 两种落地方案对比与选择

### 4.1 方案 1：统一 tool-call loop（模型在循环中自己调用 Skill）

- 所有 LocalAgent（包含 ChatAgent）升级为“tool-call loop”：
  - LLM 输出 tool call -> 执行 tool -> 回填 observation -> 再问 LLM
- 优点：最贴近 Claude Code 的交互范式；语义触发完全由模型在 loop 中完成
- 缺点：工程改造面大（ChatAgent/ParallelAgent 等需重构为 loop agent），风险高，MVP 周期长

### 4.2 方案 2：预处理式 Skill Selector（在主执行前完成语义选择 + 注入）

- 在 LocalAgent 执行前增加一段“语义选择器”：
  - 输入：用户 query + skills metadata（name/description）
  - 输出：selected skill 或 none
- 如果选中：
  - 框架调用 SkillTool 加载 SKILL.md 正文（渐进披露层级 2）
  - 将注入内容加入本次执行上下文（system/additional_prompt）
  - 再进入原 agent 的执行逻辑（ChatAgent 仍可保持单次 LLM 调用）
- 优点：改造小；可快速让所有 LocalAgent 获得“语义触发 Skill”能力；MVP 友好
- 缺点：触发效果取决于 selector 质量（需要调优与评测）；比方案 1 多一次额外 LLM 调用（成本/时延）

### 4.3 决策

MVP 采用方案 2：
- 原因：最小改造实现“全员可语义触发”；不强迫现有系统大重构
- 风险：效果可能不如 loop 方式稳定
- 缓解：通过 prompt/候选裁剪/日志与离线评测逐步优化 selector；后续可演进到方案 1

## 5. MVP 范围（Scope）

### 5.1 必做能力

- Skills discovery（目录扫描 + 优先级）
  - 兼容 `.claude/skills/<skill>/SKILL.md`（标准）
  - 保留兼容 `.oxygent/skills/<skill>/SKILL.md`（现有）
- Skills catalog 注入（metadata only）
  - 所有 LocalAgent 构建 system prompt 时可见
  - 必须过滤 `disable-model-invocation: true`（不让模型“看到并自动用”）
- Skill Selector（语义触发）
  - 适用于所有 LocalAgent（ChatAgent、ReActAgent、ParallelAgent 等）
- Skill 显式触发（manual）
  - 支持 `/skill-name args` 或 request arguments 显式指定（具体方式以实现方案为准）
- Skill 激活注入
  - `SKILL.md` body 触发时注入
  - `$ARGUMENTS` 替换规则（若正文无 `$ARGUMENTS` 则在末尾追加 `ARGUMENTS: ...`）
- 安全与约束
  - `disable-model-invocation`：不仅 catalog 过滤，也要在 SkillTool 层做强校验（防止模型直接猜名字调用）
  - `allowed-tools`：至少做到 call-time 强约束（不仅仅是 prompt 软提示）
- 留痕（可回溯）
  - trace/history 记录：discovered skills、selected_skill、invocation_source（user/model/selector）、skill_path/version、env_mods、注入长度/哈希

### 5.2 暂不做（MVP 不做或只解析不执行）

- Claude Code 的 `!` 预执行命令注入（属于 preprocessing + 安全策略，v2）
- `context: fork` + `agent: Explore/Plan/...` 的隔离子 agent 执行（v2）
- hooks 生命周期（v2）

## 6. 落地 Phase 规划（建议）

### Phase 0：规范对齐与基础设施加固（Discovery/Metadata）

交付物：
- 支持 `.claude/skills/` 与 `.oxygent/skills/` 的 discovery 与优先级
- 统一 frontmatter 解析（至少 name/description/disable-model-invocation/user-invocable/argument-hint/allowed-tools/model/timeout）
- Skill catalog 注入下沉到 LocalAgent（metadata-only）

验收：
- 任意 LocalAgent 都能在 system prompt 中看到 skills 列表（过滤 disable-model-invocation）

### Phase 1：方案 2（Skill Selector）全员语义触发

交付物：
- 在 LocalAgent 增加 pre-execute selector：
  - 选择 skill 或 none
  - 选中后调用 SkillTool 并注入正文
- 显式触发通路（用户点名 skill，不走 selector）
- trace/history 留痕字段上线

验收：
- ChatAgent 在不改成 loop 的情况下也能“语义触发 skill 并生效”
- 留痕可回溯：可看到为什么触发、触发了什么、注入了什么

### Phase 2：效果/安全强化（Quality & Policy）

交付物：
- selector 调优：候选裁剪、反例 prompt、置信度阈值、冷却机制（避免过度触发）
- allowed-tools 做强约束（执行层拦截）
- 对 `disable-model-invocation` 做双重防护（catalog + SkillTool 拒绝）

验收：
- 低误触发率；关键敏感 skill 不会被模型自动触发

### Phase 3：演进到方案 1（可选）

交付物：
- 逐步把关键 agent（如 ChatAgent）升级为 tool-call loop
- selector 作为 fallback 或用于预筛选，最终由 loop 主导

## 7. 风险与对策

- 风险：方案 2 的选择效果不稳定
  - 对策：离线评测集 + 日志回放 + prompt 迭代；引入置信度阈值与冷却
- 风险：allowed-tools 仅 prompt 软约束不安全
  - 对策：必须做 call-time 强约束
- 风险：skill 数量多导致 catalog 太长
  - 对策：metadata 字符预算；只注入 name/description；超预算做裁剪并记录告警

## 8. 与现有代码的映射（便于实现定位）

- Skills 系统初始化：`oxygent/mas.py`（`_init_skills_system`）
- Skill 工具：`oxygent/oxy/skills/skill_tool.py`
- Skill 注册与 prompt section：`oxygent/oxy/skills/skill_registry.py`
- ReActAgent 现有 skills 支持：`oxygent/oxy/agents/react_agent.py`
- LocalAgent 通用执行入口（建议加 selector）：`oxygent/oxy/agents/local_agent.py`

---

（本文为方案讨论归档，后续实现细节以 PR/ADR 更新为准）
