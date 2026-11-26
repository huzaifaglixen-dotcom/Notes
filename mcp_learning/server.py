from mcp.server.fastmcp import FastMCP
from datetime import datetime

mcp = FastMCP("Huzaifa Calculator")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Adds two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@mcp.tool()
def current_time() -> str:
    """Returns current server time"""
    return datetime.now().strftime("%H:%M:%S")

@mcp.tool()
def bmi(weight: float, height: float) -> float:
    """Calculate BMI"""
    return weight / (height * height)


if __name__ == "__main__":
    mcp.run()