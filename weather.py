import httpx


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


async def get_coordinates(city: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            GEOCODING_URL,
            params={
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json"
            }
        )

        response.raise_for_status()

        data = response.json()

        if not data.get("results"):
            raise ValueError(f"City not found: {city}")

        location = data["results"][0]

        return {
            "name": location["name"],
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "country": location.get("country")
        }

async def get_weather(city: str):
    location = await get_coordinates(city)

    async with httpx.AsyncClient() as client:
        response = await client.get(
            FORECAST_URL,
            params={
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "current": [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "apparent_temperature",
                    "precipitation",
                    "weather_code",
                    "wind_speed_10m"
                ]
            }
        )

        response.raise_for_status()

        weather = response.json()

        return {
            "location": location,
            "current": weather["current"]
        }

async def get_forecast(city: str, days: int = 3):
    print("DEBUG city:", city)
    print("DEBUG days:", days)

    location = await get_coordinates(city)

    print("DEBUG location:", location)

    async with httpx.AsyncClient() as client:
        response = await client.get(
            FORECAST_URL,
            params={
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "daily": "time,temperature_2m_max,temperature_2m_min,weather_code",
                "forecast_days": days
            }
        )

        print("DEBUG status:", response.status_code)
        print("DEBUG response:", response.text)

        response.raise_for_status()

        forecast = response.json()
        if response.status_code != 200:
            print("STATUS:", response.status_code)
            print("ERROR:", response.text)
        print("DEBUG forecast:", forecast)

        return {
            "location": location,
            "forecast": forecast["daily"]
        }

# Compatibility alias for the misspelled function name used in tests
async def get_forcast(city: str, days: int = 3):
    """Backward compatibility for tests that call the misspelled version."""
    return await get_forecast(city, days)