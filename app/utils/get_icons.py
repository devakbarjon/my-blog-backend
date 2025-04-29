def map_weather_code_to_icon(weather_code):
    if weather_code == 0:
        return "sun"
    elif weather_code in [1, 2, 3]:
        return "cloudy"
    elif weather_code in [45, 48]:
        return "stratuscumulus"
    elif 51 <= weather_code <= 67 or 80 <= weather_code <= 82:
        return "rain"
    elif 71 <= weather_code <= 77 or 85 <= weather_code <= 86:
        return "snow"
    elif 95 <= weather_code <= 99:
        return "storm"
    else:
        return "cloudy"  # default fallback
