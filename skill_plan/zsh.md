# Skill 脚本与资源运行方案（scripts / resources）

## 现状

- **SkillAgent** 只负责：发现技能（metadata）、激活技能（手动 `/skill-name` 或 selector）、将 `SKILL.md` 正文及可选 **resources** 注入到上下文；**不负责执行技能内的脚本**。
- **Resources**：通过 frontmatter 的 `resources:` 指定路径，Registry 会把这些文件/目录的**文本内容**读入并拼进注入 prompt；有文件数/大小上限，二进制默认跳过。**仅“读进 prompt”，不执行。**
- **Scripts**：技能目录下的 `scripts/` 被当作“非技能子目录”排除发现，**不会被自动发现、也不会被自动执行**。要“运行脚本”只能依赖 Agent 在激活技能后**调用已有工具**（如 `shell_tools.run_shell_command`）或**新增专用 Tool**。

## 为何“支持弱”

- 激活技能时，**没有把 skill 的真实目录路径暴露给 Agent**（`SkillTool` 返回的 `extra` 里也不含 `skill_path`），Agent 无法可靠地知道“当前技能根目录”在哪里，因此难以定位并执行 `scripts/` 下的脚本。
- 现有 `shell_tools.run_shell_command` 可执行任意命令（含 zsh/bash），但需要调用方自己提供 `base_dir` 或完整路径；若脚本放在技能目录下，调用方缺少“技能根目录”这一信息。

## 是否需要单独写 zsh/bash 支持？

- **不需要**。已有 `preset_tools/shell_tools.py` 的 `run_shell_command`（`subprocess.run(..., shell=True)`）即可执行 zsh/bash 命令。
- 问题在于**如何把“技能根目录”和“允许执行的脚本路径”**安全地交给执行端，而不是再实现一套 shell 解释器。

## 推荐落地方案

### 方案 A：最小改动（当前即可用）

- 将脚本放在**项目内固定、已知路径**（例如仓库内某固定目录），在 SKILL.md 的 instructions 里写清“如何调用该脚本（命令与参数）”。
- Agent 在技能激活后，通过 **`shell_tools.run_shell_command`** 传入该固定路径或相对项目根的路径执行即可。
- 缺点：脚本与技能解耦，技能目录下的 `scripts/` 无法被“技能感知”地执行。

### 方案 B：新增专用 Tool（推荐）

- 新增一个 **Skill 感知**的 Tool，例如：  
  `run_skill_script(skill_name, script_relpath, args)`（或等价的命名）。
- **行为**：
  - 通过 `SkillRegistry` 根据 `skill_name` 解析出该技能的 `skill_path`，取 `skill_path.parent` 作为 **技能根目录** `base_dir`。
  - 只允许执行 **`scripts/`** 下的文件（即 `script_relpath` 必须落在 `base_dir / "scripts"` 下，禁止 `..` 逃逸）。
  - 调用底层执行时使用 `base_dir` 作为工作目录，执行 `script_relpath` 对应脚本（可约定支持 `.sh`/`.zsh`，由系统默认 shell 或可配置解释器执行）。
- **优点**：  
  - 脚本与技能绑定，路径由框架解析，Agent 只需传 `skill_name` + 相对 `scripts/` 的路径；  
  - 安全边界清晰（仅限该 skill 的 `scripts/` 目录）；  
  - 不依赖“单独写 zsh/bash”，复用现有 shell 执行能力即可。

### 方案 C：MCP / 服务端执行（可选）

- 若需跨机、隔离或更强权限控制，可将“运行脚本”做成 **MCP Tool** 或服务端接口，Skill 只负责选择与编排，实际执行在远端/沙箱内完成。

## 实施优先级建议

1. **短期**：采用 **方案 A**，在 SKILL.md 中明确写出“脚本路径与调用方式”，配合现有 `shell_tools` 使用。
2. **中期**：落地 **方案 B**——在 OxyGent 内新增 `run_skill_script`（或同名）Tool，并在 Skill 激活时在 `extra` 或 prompt 中提供“当前技能名”及“如何调用 run_skill_script”的说明，使 Agent 能可靠执行技能自带 `scripts/`。
3. **按需**：若有跨机/合规需求，再考虑 **方案 C**。

## 文档与约定

- 技能目录结构建议：`<skill_dir>/SKILL.md`、`<skill_dir>/scripts/`、`<skill_dir>/references/`、`<skill_dir>/assets/`；其中 `scripts/` 仅用于可执行脚本，由 `run_skill_script` 白名单限制。
- 在 SKILL.md 的 instructions 中可写明：  
  “如需执行本技能自带脚本，请使用工具 `run_skill_script`，传入技能名与 `scripts/` 下的相对路径。”

以上方案落档于 `skill_plan/zsh.md`，便于后续实现与评审对齐。
