import asyncio
import os
import sys


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_root)

from oxygent import MAS, oxy  # noqa: E402


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

    async def _offline_response(oxy_request):
        messages = oxy_request.arguments.get("messages", [])
        query = ""
        if isinstance(messages, list) and messages:
            last = messages[-1]
            if isinstance(last, dict):
                query = str(last.get("content", ""))

        system_text = ""
        if isinstance(messages, list) and messages:
            first = messages[0]
            if isinstance(first, dict) and first.get("role") == "system":
                system_text = str(first.get("content", ""))

        skill_name = ""
        marker = "[SKILL ACTIVATED: "
        if marker in system_text:
            skill_name = system_text.split(marker, 1)[1].split("]", 1)[0].strip()

        if skill_name:
            return f"(offline demo) skill activated: {skill_name}\n\nYou said: {query}"
        return (
            "(offline demo) SkillAgent is running. "
            "Set DEFAULT_LLM_BASE_URL/DEFAULT_LLM_MODEL_NAME to enable selector.\n\n"
            f"You said: {query}"
        )

    return oxy.MockLLM(name="default_llm", func_mock_process=_offline_response)


async def main():
    base_url = os.getenv("DEFAULT_LLM_BASE_URL")
    model_name = os.getenv("DEFAULT_LLM_MODEL_NAME")
    selector_enabled = bool(base_url and model_name)

    oxy_space = [
        _build_default_llm(),
        oxy.SkillAgent(
            name="master_agent",
            llm_model="default_llm",
            enable_selector=selector_enabled,
            additional_prompt=(
                "Skills are NOT tools. Never use a skill name as tool_name. "
                "Only call tools that appear in tools_description. "
                "When a skill is activated, mention its name briefly before answering."
            ),
        ),
    ]

    async with MAS(oxy_space=oxy_space) as mas:
        print("\nDiscovered skills:")
        if mas.skill_registry:
            for s in sorted(mas.skill_registry.list_skills(), key=lambda x: x.name):
                print(f"- {s.name}: {s.description}")
        else:
            print("(no skill registry)")

        if "--web" in sys.argv:
            first_query = (
                "/skill-creator init hello-skill --path .oxygent/skills\n"
                "(Tip: you can also ask in natural language to trigger selector when enabled.)"
            )
            await mas.start_web_service(first_query=first_query)
            return

        print(
            "\nEnter queries below. Examples:\n"
            "- /skill-creator init hello-skill --path .oxygent/skills\n"
            "- I want to create a new OxyGent skill named hello-skill; please guide me.\n"
            "Type 'exit' to quit.\n"
        )

        from_trace_id = ""
        while True:
            query = input("You: ").strip()
            if query in ["exit", "quit", "bye"]:
                break
            if not query:
                continue
            payload = {"query": query, "from_trace_id": from_trace_id}
            resp = await mas.chat_with_agent(payload=payload)
            from_trace_id = resp.oxy_request.current_trace_id

            if resp.extra.get("skill_selection"):
                sel = resp.extra.get("skill_selection")
                print(f"[skill selection] {sel}")
            if resp.extra.get("skill_activation"):
                act = resp.extra.get("skill_activation")
                print(f"[skill activated] {act}")

            print("LLM:", resp.output)


if __name__ == "__main__":
    asyncio.run(main())
