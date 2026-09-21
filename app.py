"""
Clean FastAPI backend for Render.com deployment.
This file is independent of MCP dependencies.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from datetime import datetime, timedelta

from tools.weather_service import WeatherService

app = FastAPI(
    title="Weather API",
    description="Simple weather API for React frontend",
    version="1.0.0"
)

# CORS configuration for both local development and production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://weathermcp-ggmn.onrender.com",
        "https://*.onrender.com",
        "*"  # Remove in strict production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WeatherResponse(BaseModel):
    city: str
    latitude: float
    longitude: float
    time: str
    temperature_c: float
    apparent_temperature_c: float
    weather_description: str
    # Add more fields as needed


@app.get("/")
async def root():
    return {
        "message": "Weather API is running",
        "endpoints": {
            "current": "/weather/{city}",
            "forecast": "/forecast/{city}?days=3"
        }
    }


@app.get("/weather/{city}")
async def get_weather(city: str, include_forecast: bool = False):
    """Get current weather for a city"""
    try:
        service = WeatherService()
        data = await service.get_current_weather(city)
        
        if include_forecast:
            today = datetime.now().strftime("%Y-%m-%d")
            tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            forecast = await service.get_weather_by_date_range(city, today, tomorrow)
            data["forecast"] = forecast
            
        return data
    except Exception as e:
        return {"error": str(e)}, 500


@app.get("/forecast/{city}")
async def get_forecast(city: str, days: int = 3):
    """Get weather forecast for a city"""
    try:
        service = WeatherService()
        today = datetime.now().strftime("%Y-%m-%d")
        end_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
        data = await service.get_weather_by_date_range(city, today, end_date)
        return data
    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
