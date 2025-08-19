import asyncio
import os

from oxygent import MAS, Config, OxyRequest, OxyResponse, oxy

# Config.set_agent_short_memory_size(7)


Config.set_agent_llm_model("default_llm")
Config.set_server_port(8081)
Config.set_server_auto_open_webpage(False)


# def my_reflexion(response: str, oxy_request: OxyRequest) -> str:
#     print(oxy_request.arguments["short_memory"])
#     # Check if response is empty
#     if not response or len(response.strip()) == 0:
#         return "The response should not be empty. Please provide a more detailed and helpful answer."
#     return None


# def func_filter(payload: dict) -> dict:
#     payload["shared_data"] = {"k": "v"}
#     return payload


# async def my_interceptor(oxy_request: OxyRequest):
#     print(oxy_request.arguments)
#     if oxy_request.arguments.get("query") == "nihao":
#         # return "参数错误"
#         return {"code": 400, "message": "参数错误"}


def process_input(oxy_request: OxyRequest):
    oxy_request.set_query(oxy_request.get_query() + "???")
    return oxy_request


def process_output(oxy_response: OxyResponse):
    oxy_response.oxy_request.set_query(
        oxy_response.oxy_request.get_query(master_level=True)
    )
    return oxy_response


oxy_space = [
    oxy.HttpLLM(
        name="default_llm",
        api_key=os.getenv("DEFAULT_LLM_API_KEY"),
        base_url=os.getenv("DEFAULT_LLM_BASE_URL"),
        model_name=os.getenv("DEFAULT_LLM_MODEL_NAME"),
        llm_params={"temperature": 0.01},
        semaphore=4,
    ),
    # oxy.HttpLLM(
    #     name="default_llm",
    #     api_key="sk-xxx",
    #     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    #     model_name="qwen3-235b-a22b",
    #     llm_params={
    #         "temperature": 0.01,
    #         "enable_thinking": False,
    #     },
    #     semaphore=4,
    # ),
    oxy.ReActAgent(
        name="master_agent",
        is_master=True,
        llm_model="default_llm",
        # func_interceptor=my_interceptor,
        func_process_input=process_input,
        # func_reflexion=my_reflexion,
        func_process_output=process_output,
        short_memory_size=2,
    ),
]


async def main():
    async with MAS(oxy_space=oxy_space) as mas:
        await mas.start_web_service(first_query="你好")


if __name__ == "__main__":
    asyncio.run(main())
