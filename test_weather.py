import unittest
from unittest.mock import AsyncMock, patch

from weather import get_forecast, get_forcast


class GetForecastTests(unittest.TestCase):
    def test_get_forecast_returns_location_and_daily_data(self):
        async def _run():
            with patch("weather.get_coordinates", new=AsyncMock(return_value={
                "name": "Paris",
                "latitude": 48.8566,
                "longitude": 2.3522,
                "country": "France",
            })), patch("httpx.AsyncClient") as mock_client:
                mock_get = AsyncMock()
                mock_response = mock_get.return_value
                mock_response.raise_for_status.return_value = None
                mock_response.json.return_value = {
                    "daily": {
                        "time": ["2026-09-18"],
                        "temperature_2m_max": [21.1],
                        "temperature_2m_min": [15.2],
                        "weather_code": [1],
                    }
                }
                mock_client.return_value.__aenter__.return_value.get = mock_get

                result = await get_forecast("Paris", 1)

                self.assertEqual(result["location"]["name"], "Paris")
                self.assertEqual(result["forecast"]["time"], ["2026-09-18"])
                self.assertEqual(result["forecast"]["temperature_2m_max"], [21.1])

        import asyncio
        asyncio.run(_run())

    def test_get_forcast_alias_returns_same_daily_data(self):
        async def _run():
            with patch("weather.get_coordinates", new=AsyncMock(return_value={
                "name": "Rome",
                "latitude": 41.9028,
                "longitude": 12.4964,
                "country": "Italy",
            })), patch("httpx.AsyncClient") as mock_client:
                mock_get = AsyncMock()
                mock_response = mock_get.return_value
                mock_response.raise_for_status.return_value = None
                mock_response.json.return_value = {
                    "daily": {
                        "time": ["2026-09-18"],
                        "temperature_2m_max": [24.5],
                        "temperature_2m_min": [19.0],
                        "weather_code": [2],
                    }
                }
                mock_client.return_value.__aenter__.return_value.get = mock_get

                result = await get_forcast("Rome", 1)

                self.assertEqual(result["location"]["name"], "Rome")
                self.assertEqual(result["forecast"]["time"], ["2026-09-18"])
                self.assertEqual(result["forecast"]["temperature_2m_max"], [24.5])

        import asyncio
        asyncio.run(_run())


if __name__ == "__main__":
    unittest.main()
