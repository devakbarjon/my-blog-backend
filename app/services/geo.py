import httpx

async def get_location(ip_address: str):
    """
    Fetches location data based on the provided IP address.
    """
    ip = ip_address
    async with httpx.AsyncClient() as client:
        try:
            geo_url = f"http://ip-api.com/json/{ip}"
            geo_res = await client.get(geo_url)
            geo_data = geo_res.json()
        except httpx.RequestError as e:
            return {"error": f"Request error: {str(e)}"}
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
    
    return {
        "ip": ip,
        "city": geo_data.get("city"),
        "country": geo_data.get("country"),
        "lat": geo_data.get("lat"),
        "lon": geo_data.get("lon")
    }


async def get_city_coordinates(city: str):
    geocoding_url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(geocoding_url)
            response.raise_for_status()
            data = response.json()
            if not data:
                return {"error": "City not found"}
            return {
                "latitude": float(data[0]["lat"]),
                "longitude": float(data[0]["lon"])
            }
        except httpx.RequestError as e:
            return {"error": f"Request error: {str(e)}"}
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
