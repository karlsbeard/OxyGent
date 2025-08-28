import asyncio
import os

from oxygent import MAS, Config, OxyRequest, OxyResponse, oxy

Config.set_agent_llm_model("default_llm")

flag = True


def func_filter(payload: str) -> str:
    global flag
    if flag:
        payload["shared_data"] = {"k": "v"}
        flag = False
    return payload


def update_group_data(oxy_request: OxyRequest) -> OxyRequest:
    print(oxy_request.group_data)
    oxy_request.group_data["k"] = "v2"
    print(oxy_request.group_data)
    print(hex(id(oxy_request.group_data)))
    return oxy_request


def read_group_data(oxy_response: OxyResponse) -> OxyResponse:
    oxy_request = oxy_response.oxy_request
    print(oxy_request.group_data)
    return oxy_response


def update_query(oxy_request: OxyRequest) -> OxyRequest:
    print(oxy_request.group_data)
    oxy_request.group_data["k"] = "v3"
    print(oxy_request.group_data)
    print(hex(id(oxy_request.group_data)))
    return oxy_request


oxy_space = [
    oxy.HttpLLM(
        name="default_llm",
        api_key=os.getenv("DEFAULT_LLM_API_KEY"),
        base_url=os.getenv("DEFAULT_LLM_BASE_URL"),
        model_name=os.getenv("DEFAULT_LLM_MODEL_NAME"),
        llm_params={"temperature": 0.01},
        semaphore=4,
    ),
    oxy.StdioMCPClient(
        name="time",
        params={
            "command": "uvx",
            "args": ["mcp-server-time", "--local-timezone=Asia/Shanghai"],
        },
    ),
    oxy.ReActAgent(
        name="master_agent",
        sub_agents=["time_agent"],
        additional_prompt="You may get several types of tasks, please choose correct tools to finish tasks.",
        is_master=True,
        func_process_input=update_group_data,
        func_process_output=read_group_data,
    ),
    oxy.ReActAgent(
        name="time_agent",
        desc="A tool for time query.",
        additional_prompt="Do not send other information except time.",
        tools=["time"],
        func_process_input=update_query,
    ),
]


async def main():
    async with MAS(oxy_space=oxy_space, func_filter=func_filter) as mas:
        await mas.start_web_service(
            first_query="现在几点",
            welcome_message="Hi, I’m OxyGent. How can I assist you?",
        )


if __name__ == "__main__":
    asyncio.run(main())
