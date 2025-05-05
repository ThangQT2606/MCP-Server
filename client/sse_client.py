# from mcp import ClientSession
# from mcp.client.sse import sse_client
import os
from loguru import logger
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_mcp_adapters.client import sse_client, ClientSession
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.checkpoint.memory import MemorySaver


load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-preview-04-17", 
    api_key=google_api_key, 
    temperature=0.3
    )

def llm_openai(api_key: str) -> ChatOpenAI:
    """Load the OpenAI model"""
    try:
        model = ChatOpenAI(
                model="gpt-4.1-nano",
                temperature=0.2,
                api_key=api_key,
                top_p=0.1
            )
        return model
    except Exception as e:
        logger.info(f"Error loading LLM: {e}")

# model = llm_openai(api_key=openai_api_key)
async def check() -> str:
    async with sse_client("http://localhost:8000/sse") as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()

            # List avail tool
            # tools = await session.list_tools()
            # print(tools)
            tools = await load_mcp_tools(session)
            print(f"Tools: {tools}")
            # result = await session.call_tool("get_weather", {"location": "Hồ tây - Hà Nội"})
            # print(result.content)
    return tools

async def main() -> str:
    tools = await check()
    agent = create_react_agent(model=model, tools=tools, checkpointer=MemorySaver())
    while True:
        query = input("Enter your query: ")
        agent_response = await agent.ainvoke(
                        {"messages": [{"role": "user", "content": query}]}, 
                        config={"configurable": {"thread_id": 1}})
        print(agent_response["messages"][-1].content)

if __name__ == "__main__":
    import asyncio
    # asyncio.run(check())
    asyncio.run(main())