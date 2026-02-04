import asyncio
import json
import os
import re
import sys


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_root)

from oxygent import MAS, oxy, preset_tools  # noqa: E402


def _build_default_llm():
    api_key = os.getenv("DEFAULT_LLM_API_KEY")
    base_url = os.getenv("DEFAULT_LLM_BASE_URL")
    model_name = os.getenv("DEFAULT_LLM_MODEL_NAME")

    if base_url and model_name:
        return oxy.HttpLLM(
            name="default_llm",
            api_key=api_key,
            base_url=base_url,
            model_name=model_name,
        )

    async def _offline(oxy_request):
        # Minimal offline flow to demo tool wiring.
        messages = oxy_request.arguments.get("messages", [])
        system_text = ""
        if isinstance(messages, list) and messages:
            first = messages[0]
            if isinstance(first, dict) and first.get("role") == "system":
                system_text = str(first.get("content", ""))

        last = messages[-1] if isinstance(messages, list) and messages else {}
        q = str(last.get("content", "")).strip() if isinstance(last, dict) else str(last)

        m = re.search(r"\[SKILL ACTIVATED:\s*([^\]]+)\]", system_text)
        active_skill = m.group(1).strip() if m else ""

        history_text = "\n".join(
            str(m.get("content", ""))
            for m in (messages or [])
            if isinstance(m, dict) and m.get("content")
        )

        pending = "[PENDING_SKILL_INIT:" in history_text
        if pending:
            m2 = re.search(r"\[PENDING_SKILL_INIT:\s*([^\]]+)\]", history_text)
            payload = m2.group(1).strip() if m2 else ""
            if q.lower() in {"y", "yes", "确认", "是", "好", "ok"}:
                data = json.loads(payload)
                return json.dumps(
                    {
                        "tool_name": "run_skill_script",
                        "arguments": {
                            "skill_name": "skill-creator",
                            "script_relpath": "init_skill.py",
                            "args": [data["skill_name"], "--path", data["path"]],
                        },
                    },
                    ensure_ascii=False,
                )
            if q.lower() in {"n", "no", "取消", "否", "不"}:
                return "Cancelled."
            return "Please confirm: reply 'yes' to create, or 'no' to cancel."

        if active_skill == "skill-creator":
            parts = q.split()
            if parts[:1] == ["init"] and len(parts) >= 2:
                skill_name = parts[1]
                out_path = ".claude/skills"
                if "--path" in parts:
                    try:
                        out_path = parts[parts.index("--path") + 1]
                    except Exception:
                        pass
                return (
                    "Reply 'yes' to confirm skill creation, or 'no' to cancel.\n\n"
                    + "[PENDING_SKILL_INIT: "
                    + json.dumps({"skill_name": skill_name, "path": out_path}, ensure_ascii=False)
                    + "]"
                )

        return (
            "(offline demo) Try:\n"
            "- /skill-creator init hello-skill --path .claude/skills\n"
            "- /agent-browser 获取墨迹天气的今日温度"
        )

    return oxy.MockLLM(name="default_llm", func_mock_process=_offline)


async def main():
    use_web = "--web" in sys.argv

    oxy_space = [
        _build_default_llm(),
        preset_tools.file_tools,
        preset_tools.shell_tools,
        preset_tools.skill_tools,
        oxy.SkillAgent(
            name="master_agent",
            llm_model="default_llm",
            # Enable selector only when a real LLM is configured.
            enable_selector=bool(os.getenv("DEFAULT_LLM_BASE_URL") and os.getenv("DEFAULT_LLM_MODEL_NAME")),
            tools=["file_tools", "shell_tools", "skill_tools"],
            additional_prompt=(
                "If the active skill is skill-creator: ask only missing questions; "
                "ALWAYS require an explicit yes/no confirmation before calling run_skill_script. "
                "Default output path is .claude/skills (project-local).\n"
                "If the active skill describes CLI commands (e.g. agent-browser ...), execute them via "
                "run_shell_command(command=\"<full cli command>\")."
            ),
        ),
    ]

    async with MAS(oxy_space=oxy_space) as mas:
        if use_web:
            await mas.start_web_service(
                first_query="/skill-creator init hello-skill --path .claude/skills"
            )
            return

        print(
            "\nExamples:\n"
            "- /skill-creator init hello-skill --path .claude/skills\n"
            "- 帮我创建一个新的 skill，名字叫 hello-skill\n"
            "- /agent-browser 获取墨迹天气的今日温度\n"
            "Type 'exit' to quit.\n"
        )

        from_trace_id = ""
        while True:
            query = input("You: ").strip()
            if query in {"exit", "quit", "bye"}:
                break
            if not query:
                continue
            resp = await mas.chat_with_agent(
                payload={"query": query, "from_trace_id": from_trace_id}
            )
            from_trace_id = resp.oxy_request.current_trace_id
            print("LLM:", resp.output)


if __name__ == "__main__":
    asyncio.run(main())
