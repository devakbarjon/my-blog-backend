from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.services.weather import get_weather_forecast

router = APIRouter(
    prefix="/api/v1/weather",
    tags=["Weather"]
)

@router.get("/forecast")
async def get_forecast(
    city: Optional[str] = Query(None, description="City name"),
    ip_address: Optional[str] = Query(None, description="IP address")
):
    """
    Get 7-day weather forecast by city or IP address.
    """
    if not city and not ip_address:
        raise HTTPException(status_code=400, detail="Provide either city or ip_address")

    try:
        forecast = await get_weather_forecast(city=city, ip_address=ip_address)
        return forecast
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        raise HTTPException(status_code=500, detail=str(e))
