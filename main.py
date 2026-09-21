"""
FastAPI Backend for Weather Service
This provides simple REST endpoints that can be called from any React app.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import asyncio
import os
from datetime import datetime, timedelta

from tools.weather_service import WeatherService

app = FastAPI(title="Weather API", description="Simple weather API for React frontend")

# Enable CORS so React frontend can call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[                  # Local React development (your fullstack project)
        "http://localhost:5173",                    # Vite default port (common for React)
        "https://weathermcp-ggmn.onrender.com",     # Your deployed backend
        "*"                                         # Remove this in production for security
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WeatherResponse(BaseModel):
    location: dict
    current: dict
    forecast: Optional[dict] = None

@app.get("/")
async def root():
    return {"message": "Weather API is running. Try /weather/{city}"}

@app.get("/weather/{city}")
async def get_weather(city: str, include_forecast: bool = False):
    """Get current weather for a city"""
    service = WeatherService()
    data = await service.get_current_weather(city)
    
    if include_forecast:
        from datetime import datetime, timedelta
        today = datetime.now().strftime("%Y-%m-%d")
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        forecast = await service.get_weather_by_date_range(city, today, tomorrow)
        data["forecast"] = forecast
    
    return data

@app.get("/forecast/{city}")
async def get_forecast(city: str, days: int = 3):
    """Get weather forecast for a city"""
    service = WeatherService()
    data = await service.get_weather_by_date_range(city, 
                                                   (datetime.now()).strftime("%Y-%m-%d"),
                                                   (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d"))
    return data

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
