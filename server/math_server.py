# math_server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

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
def sqrt(a: int) -> int:
    """Square root of a"""
    return a ** 0.5

@mcp.tool()
def cube(a: int) -> int:
    """Cube of a"""
    return a ** 3

if __name__ == "__main__":
    print("Starting math server...")
    mcp.run(transport="stdio")