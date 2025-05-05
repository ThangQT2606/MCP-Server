import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash", 
    api_key=google_api_key, 
    temperature=0.3
    )

load_dotenv(find_dotenv(), override=True)
async def check():
    async with MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                # Make sure to update to the full absolute path to your math_server.py file
                "args": ["../server/math_server.py"],
                "transport": "stdio",
            },
            "mcp": {
                # Make sure you start your weather server on port 8000
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            }
        }
    ) as client:
        all_tools = client.get_tools()
        print(all_tools)
        agent = create_react_agent(model, client.get_tools())

        # Gọi async functions
        math_response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
        weather_response = await agent.ainvoke({"messages": "what is the weather in Nam Dinh?"})

        print("Math Response:", math_response)
        print("Weather Response:", weather_response)

# Chạy vòng lặp async
if __name__ == "__main__":
    asyncio.run(check())