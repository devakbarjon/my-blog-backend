import httpx
from app.services.geo import get_city_coordinates, get_location
from app.core.config import settings
from app.utils.get_icons import map_weather_code_to_icon
api_key = settings.openweather_api_key

async def get_weather_forecast(city: str = None, ip_address: str = None):
    if city:
        coordinates = await get_city_coordinates(city)
        if "error" in coordinates:
            return coordinates

        lat, lon = coordinates["latitude"], coordinates["longitude"]
    elif ip_address:
        location = await get_location(ip_address)
        if "error" in location:
            return location

        lat, lon = location["lat"], location["lon"]
        city = location["city"]

    forecast_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode,"
        f"relative_humidity_2m_max,windspeed_10m_max"
        f"&timezone=auto"
    )

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(forecast_url)
            response.raise_for_status()
            data = response.json()
            daily_forecast = [
                    {
                        "time": time,
                        "temperature_max": max_temp,
                        "temperature_min": min_temp,
                        "precipitation": precip,
                        "humidity": humidity,
                        "wind_speed": wind_speed,
                        "weather": [
                            {
                                "icon": map_weather_code_to_icon(code),
                                "description": "custom"
                            }
                        ]
                    }
                    for time, max_temp, min_temp, precip, code, humidity, wind_speed in zip(
                        data['daily']['time'],
                        data['daily']['temperature_2m_max'],
                        data['daily']['temperature_2m_min'],
                        data['daily']['precipitation_sum'],
                        data['daily']['weathercode'],
                        data['daily']['relative_humidity_2m_max'],
                        data['daily']['windspeed_10m_max']
                    )
                ]
            return {
                "city": city,
                "latitude": lat,
                "longitude": lon,
                "daily": daily_forecast
            }
        except httpx.RequestError as e:
            return {"error": f"Request error: {str(e)}"}
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}