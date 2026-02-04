"""SkillAgent: ReActAgent with first-class skills support.

Skill activation sources:
- Manual: user query starts with `/<skill-name> ...`
- Selector: optional extra LLM call over metadata only (name + description)

This agent never relies on the LLM to call the Skill tool.
"""

from __future__ import annotations

import logging
import re
from typing import Optional, Tuple

from pydantic import Field

from ...schemas import OxyRequest, OxyResponse, OxyState
from ..skills.skill_selector import select_skill
from .react_agent import ReActAgent

logger = logging.getLogger(__name__)


_MANUAL_SKILL_RE = re.compile(
    r"^/([a-zA-Z0-9][a-zA-Z0-9_\-]{0,127})(?:\s+(.*))?$"
)


def _append_prompt(base: str, extra: str) -> str:
    base_s = (base or "").strip()
    extra_s = (extra or "").strip()
    if not extra_s:
        return base_s
    if not base_s:
        return extra_s
    return base_s + "\n\n" + extra_s


class SkillAgent(ReActAgent):
    """A ReActAgent that can activate skills and inject them into context."""

    enable_skill_catalog: bool = Field(
        True,
        description="Whether to inject the available skills (metadata only) into the prompt.",
    )
    skill_catalog_max_entries: int = Field(
        50,
        description="Max number of skill metadata entries injected into the prompt.",
    )

    enable_selector: bool = Field(
        True,
        description="Whether to run a selector LLM call to auto-activate at most one skill.",
    )
    selector_max_candidates: int = Field(
        30,
        description="Max candidate skills passed to selector.",
    )
    selector_min_confidence: float = Field(
        0.6,
        description="Min confidence required to auto-activate a selected skill.",
    )
    selector_llm_model: Optional[str] = Field(
        None,
        description="Optional LLM model to use for selection. Defaults to llm_model.",
    )

    enable_shell_tools: bool = Field(
        True,
        description=(
            "Whether to auto-register and enable preset shell_tools (run_shell_command). "
            "This makes Codex-style skills (e.g. agent-browser) practical by default."
        ),
    )

    async def init(self):
        await self._ensure_shell_tools()
        await super().init()

    async def _ensure_shell_tools(self) -> None:
        if not self.enable_shell_tools:
            return
        if "shell_tools" in (self.except_tools or []):
            return
        mas = getattr(self, "mas", None)
        if not mas:
            return
        if not getattr(mas, "oxy_name_to_oxy", None):
            return

        if "shell_tools" not in (self.tools or []):
            self.tools.append("shell_tools")

        try:
            if "shell_tools" not in mas.oxy_name_to_oxy:
                from oxygent.preset_tools.shell_tools import shell_tools

                shell_tools.set_mas(mas)
                if hasattr(mas, "add_oxy"):
                    mas.add_oxy(shell_tools)
                else:
                    mas.oxy_name_to_oxy[shell_tools.name] = shell_tools

            if "run_shell_command" not in mas.oxy_name_to_oxy:
                hub = mas.oxy_name_to_oxy.get("shell_tools")
                if hub is not None and hasattr(hub, "init"):
                    await hub.init()
        except Exception as e:
            logger.warning(f"Failed to auto-enable shell_tools: {e}")

    def _parse_manual_invocation(self, query: str) -> Optional[Tuple[str, str]]:
        q = (query or "").strip()
        if not q.startswith("/") or q.startswith("//"):
            return None
        m = _MANUAL_SKILL_RE.match(q)
        if not m:
            return None
        skill_name = m.group(1)
        args = (m.group(2) or "").strip()
        return skill_name, args

    def _is_skill_list_query(self, query: str) -> bool:
        q = (query or "").strip().lower()
        q = re.sub(r"\s+", " ", q)
        q = q.strip(" \t\r\n\"'`.,;:!?()[]{}")

        # Deterministic skill listing should be triggered only for clear "list my skills" intents.
        exact = {
            "list skills",
            "show skills",
            "skill list",
            "skills list",
            "what skills do you have",
            "what skills do u have",
            "what skill do you have",
            "what skill do u have",
            "which skills do you have",
            "which skills do u have",
            "available skills",
            "skills available",
            "你有什么技能",
            "你有哪些技能",
            "技能列表",
        }
        if q in exact:
            return True

        # Lightweight pattern matching for short questions.
        if len(q) <= 64:
            if re.match(r"^(what|which)\s+skills?\b.*\b(do\s+)?(you|u)\s+have\b", q):
                return True
            if re.match(r"^what\s+skills?\b.*\bavailable\b", q):
                return True

        return False

    def _build_skill_catalog_prompt(self, oxy_request: OxyRequest) -> str:
        registry = getattr(oxy_request.mas, "skill_registry", None)
        if not registry:
            return ""
        if not getattr(registry, "metadata_index", None):
            try:
                registry.discover_all()
            except Exception:
                return ""

        skills = list(registry.iter_skills())
        if not skills:
            return ""
        skills_sorted = sorted(skills, key=lambda s: s.name)

        max_n = max(0, int(self.skill_catalog_max_entries))
        shown = skills_sorted if max_n == 0 else skills_sorted[:max_n]
        hidden_count = max(0, len(skills_sorted) - len(shown))

        lines: list[str] = [
            "## Available Skills (metadata only)",
            "", 
            "Invoke manually with: /<skill-name> [task-or-arguments]",
            "(Skill activation is system-driven; do not call the Skill tool directly.)",
            "",
        ]

        # If the runtime provides the script runner tool, hint it explicitly.
        try:
            if (
                hasattr(self, "permitted_tool_name_list")
                and "run_skill_script" in (self.permitted_tool_name_list or [])
            ):
                lines.extend(
                    [
                        "Tip: If an activated skill asks you to run a bundled script under its scripts/ directory,",
                        "use the tool `run_skill_script` (skill_name + script_relpath + args) instead of manual path guessing.",
                        "",
                    ]
                )
        except Exception:
            pass

        for s in shown:
            flags: list[str] = []
            if getattr(s, "disable_model_invocation", False):
                flags.append("manual-only")
            if getattr(s, "user_invocable", True) is False:
                flags.append("not-user-invocable")
            suffix = f" ({', '.join(flags)})" if flags else ""
            lines.append(f"- {s.name}: {s.description}{suffix}")
            arg_hint = getattr(s, "argument_hint", None)
            if isinstance(arg_hint, str) and arg_hint.strip():
                lines.append(f"  args: {arg_hint.strip()}")

        if hidden_count:
            lines.append(f"- ... ({hidden_count} more)")

        return "\n".join(lines)

    async def _activate_skill(
        self,
        *,
        oxy_request: OxyRequest,
        skill_name: str,
        skill_args: str,
        invocation_source: str,
    ) -> None:
        if not oxy_request.has_oxy("Skill"):
            logger.warning("Skill tool not registered; cannot activate skills")
            return

        tool_resp = await oxy_request.call(
            callee="Skill",
            arguments={
                "name": skill_name,
                "arguments": skill_args,
                "invocation_source": invocation_source,
            },
            is_send_message=False,
            is_save_history=False,
        )

        if tool_resp.state is not OxyState.COMPLETED:
            return

        injection = tool_resp.output
        if not isinstance(injection, str) or not injection.strip():
            return

        oxy_request.arguments["additional_prompt"] = _append_prompt(
            oxy_request.arguments.get("additional_prompt", ""),
            injection,
        )
        oxy_request.arguments["_skill_activation"] = tool_resp.extra

    async def _before_execute(self, oxy_request: OxyRequest) -> OxyRequest:
        oxy_request = await super()._before_execute(oxy_request)

        registry = getattr(oxy_request.mas, "skill_registry", None)
        if not registry:
            return oxy_request

        if self.enable_skill_catalog:
            oxy_request.arguments["additional_prompt"] = _append_prompt(
                oxy_request.arguments.get("additional_prompt", ""),
                self._build_skill_catalog_prompt(oxy_request),
            )

        raw_query = oxy_request.arguments.get("query", "")

        # 0) Skill list/help queries: answer deterministically from metadata.
        if self._is_skill_list_query(str(raw_query or "")):
            if not getattr(registry, "metadata_index", None):
                try:
                    registry.discover_all()
                except Exception:
                    pass
            help_text = ""
            try:
                help_text = registry.generate_user_help_section()
            except Exception:
                help_text = ""
            if isinstance(help_text, str) and help_text.strip():
                oxy_request.arguments["_skill_help_output"] = help_text
                return oxy_request

        # 1) Manual activation overrides selector.
        manual = self._parse_manual_invocation(raw_query)
        if manual:
            skill_name, args = manual
            await self._activate_skill(
                oxy_request=oxy_request,
                skill_name=skill_name,
                skill_args=args,
                invocation_source="user",
            )
            oxy_request.arguments["query"] = (
                args if args else f"Use the activated skill '{skill_name}'."
            )
            return oxy_request

        # 2) Selector activation (metadata only).
        if not self.enable_selector:
            return oxy_request

        try:
            skills = list(registry.iter_skills())
        except Exception:
            return oxy_request
        if not skills:
            return oxy_request

        selector_skills = [
            s for s in skills if not getattr(s, "disable_model_invocation", False)
        ]
        if not selector_skills:
            return oxy_request

        selection = await select_skill(
            oxy_request=oxy_request,
            llm_model=self.selector_llm_model or self.llm_model,
            skills=selector_skills,
            query=str(raw_query or ""),
            max_candidates=int(self.selector_max_candidates),
            min_confidence=float(self.selector_min_confidence),
        )

        if selection.selected_skill:
            oxy_request.arguments["_skill_selection"] = {
                "selected_skill": selection.selected_skill,
                "confidence": selection.confidence,
                "reason": selection.reason,
            }
            await self._activate_skill(
                oxy_request=oxy_request,
                skill_name=selection.selected_skill,
                skill_args="",
                invocation_source="selector",
            )

        return oxy_request

    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        help_text = oxy_request.arguments.get("_skill_help_output")
        if isinstance(help_text, str) and help_text.strip():
            return OxyResponse(state=OxyState.COMPLETED, output=help_text)
        return await super()._execute(oxy_request)

    async def _after_execute(self, oxy_response: OxyResponse) -> OxyResponse:
        oxy_request = oxy_response.oxy_request
        if oxy_request:
            if "_skill_activation" in oxy_request.arguments:
                oxy_response.extra.setdefault(
                    "skill_activation", oxy_request.arguments.get("_skill_activation")
                )
            if "_skill_selection" in oxy_request.arguments:
                oxy_response.extra.setdefault(
                    "skill_selection", oxy_request.arguments.get("_skill_selection")
                )
        return await super()._after_execute(oxy_response)
