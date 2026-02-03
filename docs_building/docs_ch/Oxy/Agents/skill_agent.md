
## 概述

`SkillAgent` 是 OxyGent 框架中的“技能增强智能体”。它的核心职责不是“执行技能脚本”，而是：

1. **发现技能（metadata-only）**：扫描技能目录并只加载 `name/description` 等轻量元数据。
2. **激活技能（system-driven）**：通过 **用户显式 `/skill-name ...`** 或 **selector（额外一次 LLM 选择）** 决定是否激活技能。
3. **注入上下文（prompt injection）**：激活后将 `SKILL.md` 的正文（以及可选 resources）作为上下文注入到 `${additional_prompt}`，让后续 LLM/工具调用在技能约束下继续执行。

> 重要：本实现 **不允许模型直接调用 `Skill` 工具**（`SkillTool` 会阻止 `invocation_source=model`），避免“模型自发开技能”。


## 本次改动总览（仓库变更摘要）

本次落地 SkillAgent/Skills Runtime 相关改动主要包括：

1. **新增 Skills Runtime（progressive disclosure）**：
   - `oxygent/oxy/skills/skill_registry.py`：技能发现/元数据索引/按需加载全文 + 资源目录加载限制
   - `oxygent/oxy/skills/skill_metadata.py`：metadata 结构（含 disable-model-invocation / user-invocable 等）
   - `oxygent/oxy/skills/skill_content.py`：全文结构、注入格式、environment_modifications 解析
   - `oxygent/oxy/skills/skill_tool.py`：工具名固定为 `Skill`，负责加载全文并返回注入内容
   - `oxygent/oxy/skills/skill_selector.py`：metadata-only 的 selector（额外一次 LLM 调用返回 strict JSON）

2. **新增 SkillAgent + 导出**：
   - `oxygent/oxy/agents/skill_agent.py`：在 `_before_execute()` 做 catalog 注入 + 激活；在 `_after_execute()` 回填 extra
   - `oxygent/oxy/agents/__init__.py`、`oxygent/oxy/__init__.py`：导出 `SkillAgent`

3. **MAS 侧 wiring**：
   - `oxygent/mas.py`：增加 `mas.skill_registry`，并在 `MAS.init()` 中自动创建 `SkillRegistry`、注册/绑定 `SkillTool(name="Skill")`

4. **示例与测试**：
   - `examples/agents/demo_skill_agent.py`：提供对话式 Demo（CLI/可选 Web），并修复运行路径问题
   - `test/unittest/test_skill_registry.py`：覆盖 discovery/precedence/资源目录限制等
   - `test/unittest/test_skill_agent.py`：覆盖手动激活、selector 激活、手动覆盖 selector

5. **其他兼容/稳定性修复（非 SkillAgent 核心，但与测试/示例相关）**：
   - `oxygent/chart/*`：为 `oxygent.chart.*` 提供兼容导入路径（对齐 integration test）
   - `oxygent/databases/db_redis/jimdb_ap_redis.py`：aioredis import 保护，避免在某些 Python 版本下 import 直接炸测试
   - `examples/agents/parallel_demo.py`：避免 integration test 启动阻塞式 web service；无环境变量时用 `MockLLM` 离线输出


## SkillAgent 能做什么

1. **让用户通过统一的“技能目录 + 手动指令”使用技能**：`/<skill-name> [arguments]`
2. **让系统通过 selector 自动选择（最多一个）技能并激活**（可开关）
3. **将技能正文/资源作为上下文注入**，使后续对话/工具调用遵循技能工作流
4. **把选中/激活信息写入 `OxyResponse.extra`**，便于日志与 UI 展示


## SkillAgent 的实现细节（关键流程）

### 1）MAS 侧：SkillRegistry + SkillTool wiring

在 `MAS.init()` 中：

- 若 `mas.skill_registry` 为空：创建 `SkillRegistry(auto_discover=True)`
- 若 MAS 未注册名为 `Skill` 的 tool：注册 `SkillTool()`
- 若已存在 `SkillTool`：通过 `set_registry()` 绑定 registry

因此在正常 MAS 启动时：

- `oxy_request.mas.skill_registry` 总是可用（如果初始化成功）
- `SkillTool` 可以通过 `oxy_request.mas.skill_registry` 找到 registry


### 2）SkillAgent：在 `_before_execute()` 激活并注入

`SkillAgent` 继承 `ReActAgent`，但技能逻辑主要发生在 **执行前 hook**：

1. `await super()._before_execute()`：让 `LocalAgent` 先把 `tools_description`、基础 `additional_prompt` 等准备好
2. 注入“技能目录”（metadata-only）：追加到 `oxy_request.arguments["additional_prompt"]`
3. **手动激活优先**：若用户 query 满足 `/skill-name ...`：
   - 调用 `Skill` 工具：`invocation_source="user"`
   - 把 `SkillTool` 返回的注入文本追加到 `additional_prompt`
   - 将 `query` 重写为“arguments 部分”（避免 LLM 继续看到 `/skill-name`）
4. 若未手动激活且 `enable_selector=True`：
   - 调用 `select_skill(...)`（metadata-only）得到 `{selected_skill, confidence, reason}`
   - 置信度达阈值后调用 `Skill` 工具：`invocation_source="selector"`
   - 将注入文本追加到 `additional_prompt`

并在 `_after_execute()` 将以下字段回填到响应里：

- `OxyResponse.extra["skill_selection"]`
- `OxyResponse.extra["skill_activation"]`


### 3）SkillTool：只负责“加载 + 注入”，不执行技能任务

`SkillTool` 的行为：

- 通过 registry 按需加载技能全文（progressive disclosure）
- 生成注入内容：`SkillContent.to_context_injection()`（包含 `[SKILL ACTIVATED: name]` 标记）
- 替换 `$ARGUMENTS`（若提供 arguments）
- 严格限制调用源：
  - `invocation_source=model`：直接 `SKIPPED`
  - `disable-model-invocation=true`：阻止 selector 激活
  - `user-invocable=false`：阻止用户 `/skill-name` 手动激活

返回：

- `output`：注入字符串
- `extra.environment_modifications`：当前支持解析 `allowed_tools/model/timeout`（由 skill frontmatter 提供）

> 说明：本版本 SkillAgent 主要使用“注入 prompt”，`environment_modifications` 目前仅透出在 `extra`，未对 agent 运行时做强制应用。


## 手动激活语法

- 格式：`/<skill-name> [arguments]`
- skill-name：`[a-zA-Z0-9][a-zA-Z0-9_\-]{0,127}`
- `//...` 会被当作普通文本（用于转义）

示例：

```text
/skill-creator init hello-skill --path .oxygent/skills
```


## Selector 自动激活（metadata-only）

当 `enable_selector=True` 且没有手动激活时：

- selector 会把“用户 query + 候选 skills（name: description）”发给 LLM
- 期望返回 **严格 JSON**：

```json
{
  "selected_skill": "<name>" | null,
  "confidence": 0.0,
  "reason": "..."
}
```

- 低于 `selector_min_confidence` 时不激活技能


## 参数配置

`SkillAgent` 关键参数：

| 参数 | 类型 | 默认值 | 说明 |
|---|---:|---:|---|
| `enable_skill_catalog` | bool | `True` | 是否注入“可用技能目录（metadata-only）” |
| `skill_catalog_max_entries` | int | `50` | 注入技能条目上限（0 表示不截断） |
| `enable_selector` | bool | `True` | 是否启用 selector 自动激活 |
| `selector_max_candidates` | int | `30` | 送入 selector 的候选技能数 |
| `selector_min_confidence` | float | `0.6` | 自动激活阈值 |
| `selector_llm_model` | str\|None | `None` | selector 用的 LLM，默认用 agent 的 `llm_model` |


## 使用示例

### 1）命令行对话式 Demo

```bash
python examples/agents/demo_skill_agent.py
```

### 2）Web 对话（可选）

```bash
python examples/agents/demo_skill_agent.py --web
```

### 3）环境变量

如果希望启用 selector（需要可用的 LLM）：

- `DEFAULT_LLM_BASE_URL`
- `DEFAULT_LLM_MODEL_NAME`
- （可选）`DEFAULT_LLM_API_KEY`


## 常见问题

### Q1：为什么模型输出里出现 `tool_name: "skill-creator"`？

Skill 是“注入上下文”，不是 MAS 里可调用的 tool。为了避免模型把 skill 当 tool，本仓库的约束是：

- Skill 激活只能通过系统调用 `Skill` tool
- Demo 里也增加了 prompt 约束：**Never use a skill name as tool_name**

### Q2：为什么会提示 skill 重名覆盖？

`SkillRegistry` 的搜索路径有优先级，后面的目录会覆盖前面目录的同名 skill（例如 `.claude/skills` 可能覆盖 `.oxygent/skills`）。

### Q3：如何查看当前有哪些 skills？

建议使用显式命令：`list skills`。

这类问题本质是“**列出 metadata**”，不是“激活某个 skill”。在未做专门处理时，可能出现：

1. **模型倾向于调用 Tool**：它看到 toolset 里存在 `Skill`，会尝试用它来“列出技能”，但 `Skill` 设计上需要 `name`，并且模型调用也会被拦截（`SKIPPED`），最终容易输出含糊答案。
2. **Prompt 依从性/截断**：即使已经注入了“技能目录”，模型也可能忽略该段（尤其在上下文很长时）。
3. **实际未使用 SkillAgent**：如果 master agent 不是 `SkillAgent`，就不会有 catalog 注入与相关拦截逻辑。

当前实现：

- 用 `/<skill-name> ...` 明确激活。
- 用 `list skills`：`SkillAgent` 会直接从 `SkillRegistry` 的 metadata 生成用户可读的 skills 列表（不加载全文）。
