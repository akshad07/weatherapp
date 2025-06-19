import requests
from .models import WeatherForecast
from django.conf import settings
from datetime import datetime
from django.utils.timezone import get_current_timezone

def fetch_and_store_forecast(lat, lon, location):
    """
    Fetch forecast data from OpenWeatherMap for the given location and save it.
    """
    api_key = settings.WEATHER_API_KEY
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch forecast: {response.status_code}")
        return

    data = response.json()
    for entry in data.get("list", []):
        main = entry.get("main", {})
        weather = entry.get("weather", [{}])[0]
        wind = entry.get("wind", {})
        clouds = entry.get("clouds", {})
        rain = entry.get("rain", {})

        WeatherForecast.objects.create(
            location=location,
            datetime=entry.get("dt_txt"),
            temp=main.get("temp"),
            feels_like=main.get("feels_like"),
            temp_min=main.get("temp_min"),
            temp_max=main.get("temp_max"),
            humidity=main.get("humidity"),
            pressure=main.get("pressure"),
            weather_main=weather.get("main"),
            weather_description=weather.get("description"),
            icon=weather.get("icon"),
            clouds=clouds.get("all"),
            wind_speed=wind.get("speed"),
            wind_deg=wind.get("deg"),
            visibility=entry.get("visibility"),
            pop=entry.get("pop"),
            rain_3h=rain.get("3h")
        )


def get_current_weather(lon, lat):
    api_key = settings.WEATHER_API_KEY
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'units': 'metric'
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        print("Request URL:", response.url)

        data = response.json()

        tz = get_current_timezone()

        sunrise_unix = data["sys"].get("sunrise")
        sunset_unix = data["sys"].get("sunset")
        print("sunrise_unix :",sunrise_unix)
        print("sunset_unix :",sunset_unix)

        # Handle None or 0 safely
        sunrise_str = datetime.fromtimestamp(sunrise_unix, tz).strftime('%H:%M') if sunrise_unix else "N/A"
        sunset_str = datetime.fromtimestamp(sunset_unix, tz).strftime('%H:%M') if sunset_unix else "N/A"

        return {
            "city": data.get("name", "Unknown"),
            "datetime": data.get("dt"),
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "temp_min": data["main"]["temp_min"],
            "temp_max": data["main"]["temp_max"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "weather_main": data["weather"][0]["main"],
            "weather_description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"],
            "clouds": data["clouds"]["all"],
            "wind_speed": data["wind"]["speed"],
            "wind_deg": data["wind"]["deg"],
            "visibility": data.get("visibility"),
            "sunrise": sunrise_str,
            "sunset": sunset_str,
        }

    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None


def format_forecast_response(location, forecasts):
    simplified_data = []

    for forecast in forecasts:
        simplified_data.append({
            "timestamp": int(forecast.datetime.timestamp()),
            "temperature": {
                "current": forecast.temp,
                "min": forecast.temp_min,
                "max": forecast.temp_max
            },
            "feels_like": forecast.feels_like,
            "condition": forecast.weather_main,
            "description": forecast.weather_description,
            "humidity": forecast.humidity,
            "wind": {
                "speed_kmh": forecast.wind_speed * 3.6,  # optional: convert to km/h
                "direction_deg": forecast.wind_deg
            },
            "cloudiness_percent": forecast.clouds,
            "rain_mm": forecast.rain_3h or 0,
            "datetime": forecast.datetime.strftime("%Y-%m-%d %H:%M")
        })

    return {
        "location": {
            "id": location.id,
            "name": location.name,
            "coordinates": {
                "lat": location.point.y,
                "lon": location.point.x
            }
        },
        "forecasts": simplified_data
    }


def get_current_weather_data(lon, lat):
    api_key = settings.WEATHER_API_KEY
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'units': 'metric'
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

    weather = data.get("weather", [{}])[0]
    rain = data.get("rain", {}).get("1h", 0) or 0

    return {
        "location": {
            "id": data.get("id"),
            "name": data.get("name"),
            "coordinates": {
                "lat": data.get("coord", {}).get("lat"),
                "lon": data.get("coord", {}).get("lon")
            }
        },
        "weather": {
            "timestamp": data.get("dt"),
            "temperature": {
                "current": data["main"]["temp"],
                "min": data["main"].get("temp_min"),
                "max": data["main"].get("temp_max")
            },
            "feels_like": data["main"]["feels_like"],
            "condition": weather.get("main"),
            "description": weather.get("description"),
            "humidity": data["main"]["humidity"],
            "wind": {
                "speed_kmh": data["wind"]["speed"] * 3.6,
                "direction_deg": data["wind"].get("deg")
            },
            "cloudiness_percent": data.get("clouds", {}).get("all"),
            "rain_mm": rain,
            "datetime": datetime.fromtimestamp(data["dt"]).strftime("%Y-%m-%d %H:%M")
        }
    }

def fetch_forecast_data(lon, lat):
    """
    Fetch and format forecast data from OpenWeatherMap.
    """
    api_key = settings.WEATHER_API_KEY
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        raw_data = response.json()
    except requests.RequestException as e:
        print(f"Error fetching forecast data: {e}")
        return None

    city_info = raw_data.get("city", {})
    forecasts = raw_data.get("list", [])

    custom_forecast_list = []
    for item in forecasts:
        weather = item.get("weather", [{}])[0]
        rain_3h = item.get("rain", {}).get("3h", 0)

        custom_forecast_list.append({
            "timestamp": item.get("dt"),
            "temperature": {
                "current": item["main"]["temp"],
                "min": item["main"]["temp_min"],
                "max": item["main"]["temp_max"]
            },
            "feels_like": item["main"]["feels_like"],
            "condition": weather.get("main"),
            "description": weather.get("description"),
            "humidity": item["main"]["humidity"],
            "wind": {
                "speed_kmh": item["wind"]["speed"] * 3.6,
                "direction_deg": item["wind"].get("deg")
            },
            "cloudiness_percent": item["clouds"]["all"],
            "rain_mm": rain_3h,
            "datetime": datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M")
        })

    return {
        "location": {
            "id": city_info.get("id"),
            "name": city_info.get("name"),
            "coordinates": {
                "lat": city_info.get("coord", {}).get("lat"),
                "lon": city_info.get("coord", {}).get("lon")
            }
        },
        "forecasts": custom_forecast_list
    }


