# math_server.py
from mcp.server.fastmcp import FastMCP
from typing import Literal, Union

mcp = FastMCP("Math")

@mcp.tool()
def add(a: Union[float, int], b: Union[float, int]) -> Union[float, int]:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: Union[float, int], b: Union[float, int]) -> Union[float, int]:
    """Multiply two numbers"""
    return a * b

@mcp.tool()
def subtract(a: Union[float, int], b: Union[float, int]) -> Union[float, int]:
    """Subtract two numbers"""
    return a - b

@mcp.tool()
def divide(a: Union[float, int], b: Union[float, int]) -> Union[float, int]:
    """Divide two numbers"""
    return a / b

@mcp.tool()
def power(a: Union[float, int], b: Union[float, int]) -> Union[float, int]:
    """Raise a to the power of b"""
    return a ** b

@mcp.tool()
def sqrt(a: Union[float, int]) -> Union[float, int]:
    """Square root of a"""
    return a ** 0.5

@mcp.tool()
def cube(a: Union[float, int]) -> Union[float, int]:
    """Cube of a"""
    return a ** 3

if __name__ == "__main__":
    print("Starting math server...")
    mcp.run(transport="stdio")