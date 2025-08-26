# OxyGent 项目分析报告

## 项目概述

**OxyGent** 是一个由京东开源的先进Python框架，专门用于构建生产就绪的多智能体系统。它提供了一种模块化的
方法来创建能够协作、规划和执行复杂任务的智能体团队。

## 核心设计原则

### 1. **模块化架构（"Oxy"组件）**

- OxyGent中的一切都是"Oxy" - 一个可以是智能体、工具、LLM或流程的标准化组件
- 组件像乐高积木一样组合，实现系统的快速组装
- 支持热插拔和跨场景重用

### 2. **多智能体系统（MAS）**

- 管理所有Oxy组件的中央调度器
- 处理组件间的注册、初始化和通信
- 提供Web界面、CLI和批处理模式

### 3. **层次化智能体组织**

- 主智能体协调子智能体
- 灵活的组织结构（树状层次结构）
- 自动依赖映射和可视化调试

## 核心组件

### 主要类

- **`Oxy`** (oxygent/oxy/base_oxy.py:26): 所有组件的抽象基类
  - **`MAS`** (oxygent/mas.py:58): 多智能体系统调度器
- **`BaseAgent`** (oxygent/oxy/agents/base_agent.py:21): 所有智能体的基础类
- **`OxyRequest/OxyResponse`**: 组件间通信的消息传递对象

### 智能体类型

- **`ChatAgent`**: 带有自定义提示的直接LLM交互
- **`ReActAgent`**: 推理和行动，支持工具使用
- **`ParallelAgent`**: 多个子智能体的并发执行
  - **`WorkflowAgent`**: 自定义工作流执行和子智能体协调
- **`RemoteAgent`**: 分布式智能体执行

### 工具与集成

- **MCP（模型上下文协议）** 支持外部工具
- **Function Tools**: Python函数封装为工具
- **HTTP Tools**: REST API集成
- **数据库支持**: Elasticsearch、Redis、向量数据库

## 使用方法

### 基础设置

```python
from oxygent import MAS, Config, oxy
import os

# 配置LLM
Config.set_agent_llm_model("default_llm")

# 定义Oxy空间（组件）
oxy_space = [
    oxy.HttpLLM(
        name="default_llm",
        api_key=os.getenv("DEFAULT_LLM_API_KEY"),
        base_url=os.getenv("DEFAULT_LLM_BASE_URL"),
        model_name=os.getenv("DEFAULT_LLM_MODEL_NAME"),
    ),
    oxy.ReActAgent(
        name="master_agent",
        is_master=True,
        tools=["time_tools", "file_tools"]
    )
]

# 启动系统
async def main():
    async with MAS(oxy_space=oxy_space) as mas:
        await mas.start_web_service(
            first_query="现在是什么时间？"
        )
```

### 使用模式

1. **Web服务**: `await mas.start_web_service()` - 启动FastAPI  SSE Web界面
2. **CLI模式**: `await mas.start_cli_mode()` - 交互式命令行
3. **批处理**: `await mas.start_batch_processing(queries)` - 处理多个查询
4. **直接调用**: `await mas.call(callee="agent_name", arguments={...})` - 程序化执行

### 环境配置

```bash
export DEFAULT_LLM_API_KEY="你的API密钥"
export DEFAULT_LLM_BASE_URL="你的基础URL"
export DEFAULT_LLM_MODEL_NAME="你的模型名称"
```

## 核心架构

### 数据流

1. **请求处理**: OxyRequest → 预处理 → 执行 → 后处理 → OxyResponse
2. **消息传递**: 组件通过结构化的请求/响应对象通信
3. **追踪管理**: 完整的执行追踪存储在Elasticsearch中用于调试/训练
4. **内存管理**: 基于Redis后端的短期和长期内存支持

### 关键特性

- **异步/等待**: 完全异步执行，带有基于信号量的并发控制
- **错误处理**: 重试逻辑、超时管理、优雅的错误恢复
- **可观察性**: 全面的日志记录、追踪存储和基于Web的可视化
- **可扩展性**: 自定义智能体、工具和流程的插件架构
- **分布式**: 支持远程智能体和分布式执行

   该框架在GAIA基准测试中获得59.14分，展示了在复杂多智能体场景中的强大性能。

## 如何创建自定义智能体

### 1. 继承BaseAgent创建自定义智能体

```python
from oxygent.oxy.agents.base_agent import BaseAgent
from oxygent.schemas import OxyRequest, OxyResponse, OxyState

class MyCustomAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.category = "agent"

    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        # 实现你的自定义逻辑
        query = oxy_request.get_query()

        # 处理逻辑
        result = f"自定义智能体处理: {query}"

        return OxyResponse(
            state=OxyState.FINISHED,
            output=result
        )

    # 使用自定义智能体
    oxy_space = [
        oxy.HttpLLM(name="default_llm", ...),
        MyCustomAgent(name="my_agent", desc="我的自定义智能体")
    ]
```

### 2. 创建Function Tool智能体

```python
from oxygent import oxy
from pydantic import Field

# 创建函数工具集合
fh = oxy.FunctionHub(name="my_tools")

@fh.tool(description="计算两个数的和")
async def add_numbers(a: int = Field(description="第一个数"),
                        b: int = Field(description="第二个数")):
    return a  b

@fh.tool(description="获取天气信息")
async def get_weather(city: str = Field(description="城市名称")):
    # 这里可以调用天气API
    return f"{city}的天气晴朗"

# 在oxy_space中使用
oxy_space = [
    oxy.HttpLLM(name="default_llm", ...),
    fh,  # 添加函数工具集合
    oxy.ReActAgent(
        name="tool_agent",
        tools=["my_tools"],
        desc="使用自定义工具的智能体"
    )
]
```

### 3. 创建专门的ChatAgent

```python
# 创建专业的ChatAgent
domain_expert = oxy.ChatAgent(
    name="domain_expert",
    llm_model="default_llm",
    description="领域专家智能体",
    prompt="""你是一个专业的领域专家。

   分析框架:
   1. 深入理解用户问题
   2. 提供专业的分析和建议
   3. 给出具体的行动方案
   
   请用结构化的方式回答问题。"""
)

oxy_space = [
    oxy.HttpLLM(name="default_llm", ...),
    domain_expert
]
```

### 4. 使用MCP工具创建智能体

```python
# 使用MCP客户端
mcp_client = oxy.StdioMCPClient(
    name="my_mcp_tool",
    params={
        "command": "python",
        "args": ["path/to/your/mcp_server.py"]
    }
)

agent_with_mcp = oxy.ReActAgent(
    name="mcp_agent",
    tools=["my_mcp_tool"],
    desc="使用MCP工具的智能体"
)

oxy_space = [
    oxy.HttpLLM(name="default_llm", ...),
    mcp_client,
    agent_with_mcp
]
```

## 智能体商店/市场信息

    ### 目前状态

**目前OxyGent没有官方的智能体商店或市场**，但你可以通过以下方式获取和分享智能体：

### 1. 内置预设工具

OxyGent提供了一些内置的预设工具：

- `preset_tools.time_tools` - 时间工具
- `preset_tools.file_tools` - 文件操作工具  
- `preset_tools.request_tools` - HTTP请求工具
- `preset_tools.sql_tools` - SQL数据库工具
- `preset_tools.baidu_search_tools` - 百度搜索工具

### 2. MCP生态系统

OxyGent支持MCP（Model Context Protocol），你可以使用：

- [MCP服务器列表](https://github.com/modelcontextprotocol/servers) - 官方MCP服务器
- 社区开发的MCP工具
- 自己开发MCP服务器

### 3. 示例和模板

- 查看 `examples/` 目录下的各种示例
- 参考 `mcp_servers/` 目录下的MCP工具实现
- 学习 `oxygent/preset_tools/` 中的工具实现

### 4. 社区资源

- [GitHub仓库](https://github.com/jd-opensource/OxyGent) - 查看Issues和Discussions
- [官方文档](http://oxygent.jd.com/docs/) - 详细的开发指南
- 贡献代码和智能体到主仓库

### 5. 创建你自己的智能体生态

你可以：

1. Fork OxyGent仓库并添加你的智能体
2. 创建独立的Python包发布你的智能体
3. 建立团队内部的智能体库
4. 与社区分享你的智能体实现

### 快速开始建议

1. 先从内置的预设工具开始学习
2. 查看examples目录下的各种示例
3. 尝试创建简单的Function Tool
4. 逐步发展为复杂的自定义智能体
5. 考虑使用MCP协议集成外部工具

OxyGent的设计哲学是让开发者能够快速创建和组合智能体，虽然没有中心化的商店，但其模块化设计让智能体的创建和分享变得非常灵活。
