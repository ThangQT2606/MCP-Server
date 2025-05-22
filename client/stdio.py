import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters, ServerSession
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# google_api_key = os.getenv("GOOGLE_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
model = ChatOpenAI(model="gpt-4.1", api_key=openai_api_key, temperature=0.3)
# model = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash-preview-04-17", 
#     api_key=google_api_key, 
#     temperature=0.3
#     )
print(Path(__file__).parent.parent/"server"/"math_server.py")
print(type(Path(__file__).parent.parent/"server"/"math_server.py"))
async def main():
    server_params = StdioServerParameters(
        command="python",
        # Make sure to update to the full absolute path to your math_server.py file
        args=["../server/math_server.py"],
    )

    async with stdio_client(server_params) as streams:
        async with ClientSession(*streams) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)

            # Create and run the agent
            agent = create_react_agent(model=model, tools=tools)
            agent_response = await agent.ainvoke({"messages": "Tính 1/3 + 1/3 + 1/3 + 1/3? Và bạn dùng những tools nào?"})

            print(agent_response["messages"][-1].content)

# Start the async event loop
if __name__ == "__main__":
    asyncio.run(main())
