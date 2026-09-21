from mcp.server.mcpserver import MCPServer
from weather import get_weather as fetch_weather, get_forecast as fetch_forecast

mcp = MCPServer("Weather Server")


@mcp.tool()
def hello(name: str) -> str:
    """Say hello to a person."""
    return f"Hello, {name}!"



if __name__ == "__main__":
    mcp.run()

@mcp.tool()
async def get_weather(city: str) -> dict:
    """
    Get the current weather for a city.
    """
    return await fetch_weather(city)

@mcp.tool()
async def get_forecast(
    city: str,
    days: int = 3
) -> dict:
    """
    Get the weather forecast for a city for a number of days.
    """
    return await fetch_forecast(city, days)