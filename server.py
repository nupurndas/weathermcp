"""
Simple MCP Weather Server using the official @mcp.tool() pattern.
This is the recommended style for the currently installed mcp package.
"""
import logging
from mcp.server.mcpserver import MCPServer
from tools.weather_service import WeatherService

logger = logging.getLogger("mcp-weather")
mcp = MCPServer("mcp-weather-server")


@mcp.tool()
async def get_current_weather(city: str) -> str:
    """Get current weather for a city."""
    service = WeatherService()
    data = await service.get_current_weather(city)
    return service.format_current_weather_response(data)


@mcp.tool()
async def get_weather_by_date_range(city: str, start_date: str, end_date: str) -> str:
    """Get weather for a date range."""
    service = WeatherService()
    data = await service.get_weather_by_date_range(city, start_date, end_date)
    return service.format_weather_range_response(data)


@mcp.tool()
async def get_weather_details(city: str, include_forecast: bool = False) -> dict:
    """Get detailed weather data as JSON."""
    service = WeatherService()
    data = await service.get_current_weather(city)
    if include_forecast:
        from datetime import datetime, timedelta
        today = datetime.now().strftime("%Y-%m-%d")
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        forecast = await service.get_weather_by_date_range(city, today, tomorrow)
        data["forecast"] = forecast
    return data


if __name__ == "__main__":
    mcp.run()

async def run_server(mode: str, host: str = "0.0.0.0", port: int = 8080, debug: bool = False, stateless: bool = False):
    """
    Unified server runner that supports stdio, SSE, and streamable-http modes.

    Args:
        mode: Server mode ("stdio", "sse", or "streamable-http")
        host: Host to bind to (HTTP modes only)
        port: Port to listen on (HTTP modes only)
        debug: Whether to enable debug mode
        stateless: Whether to use stateless mode (streamable-http only)
    """
    if mode == "stdio":
        logger.info("Starting stdio server...")

        from mcp.server.stdio import stdio_server

        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )

    elif mode == "sse":

        logger.info(f"Starting SSE server on {host}:{port}...")

        # Create Starlette app with SSE transport
        starlette_app = create_starlette_app(app, debug=debug)

        # Configure uvicorn
        config = uvicorn.Config(
            app=starlette_app,
            host=host,
            port=port,
            log_level="debug" if debug else "info"
        )

        # Run the server
        server = uvicorn.Server(config)
        await server.serve()

    elif mode == "streamable-http":

        mode_desc = "stateless" if stateless else "stateful"
        logger.info(f"Starting Streamable HTTP server ({mode_desc}) on {host}:{port}...")
        logger.info(f"Endpoint: http://{host}:{port}/mcp")


        starlette_app = create_streamable_http_app(app, debug=debug, stateless=stateless)

        # Configure uvicorn
        config = uvicorn.Config(
            app=starlette_app,
            host=host,
            port=port,
            log_level="debug" if debug else "info"
        )

        # Run the server (session manager lifecycle is handled by lifespan)
        server = uvicorn.Server(config)
        await server.serve()

    else:
        raise ValueError(f"Unknown mode: {mode}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())