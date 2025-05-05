
import os
import asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver, InMemorySaver

# Load environment variables
load_dotenv()

async def main():
    # Initialize the language model
    model = ChatOpenAI(model="gpt-4o")
    
    # Connect to multiple MCP servers
    async with MultiServerMCPClient(
        {
            "mcp": {
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            },
            "milvus": {
                "url": "http://localhost:8080/sse",
                "transport": "sse",
            }
        }
    ) as client:
        # Get all tools from both servers
        tools = client.get_tools()
        
        # Create the agent with all loaded tools
        agent = create_react_agent(model=model, 
                                   tools=tools,
                                   checkpointer=InMemorySaver(),)
        
        print(f"Tools loaded: \n{tools}")
        
        while True:
            # Get user input
            user_input = input("Enter your query: ")
            
            # Check for exit command
            if user_input.lower() in ["exit", "quit"]:
                break
            
            # Invoke the agent with the user input
            response = await agent.ainvoke(
                                {"messages": [{"role": "user", "content": user_input}]}, 
                                config={"configurable": {"user_id": 1, "thread_id": 1}})
            
            # Print the response from the agent
            print(f'Agent response: {response["messages"][-1].content}')

        
if __name__ == "__main__":
    asyncio.run(main())