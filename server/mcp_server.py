import os
from typing import Annotated
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from langchain_community.utilities import SerpAPIWrapper
from langchain_experimental.utilities import PythonREPL

load_dotenv()
serp = SerpAPIWrapper(serpapi_api_key=os.getenv("SERPAPI_API_KEY"))
repl = PythonREPL()
mcp = FastMCP(name="MCP Server")
mcp.settings.port = 3000

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@mcp.tool() 
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    return a - b

@mcp.tool()
def divide(a: int, b: int) -> int:
    """Divide two numbers"""
    return a / b

@mcp.tool()
def power(a: int, b: int) -> int:
    """Raise a to the power of b"""
    return a ** b

@mcp.tool()
async def python_repl_tool(code: Annotated[str, "The python code to execute to generate your chart."]):
    """Use this to execute python code and do math. If you want to see the output of a value,
    you should print it out with `print(...)`. This is visible to the user."""
    try:
        result = repl.run(code)
    except BaseException as e:
        return f"Failed to execute. Error: {repr(e)}"
    result_str = f"Successfully executed:\n```python\n{code}\n```\nStdout: {result}"
    return result_str

@mcp.tool() 
async def get_infor(query: str) -> str:
    """Search for information on the web"""
    try:
        return await serp.arun(query=query)
    except Exception as e:
        return f"Failed to get information. Error: {repr(e)}"

if __name__ == "__main__":
    print("Starting MCP server...")
    mcp.run(transport="sse")