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
    forecast_list = []

    for forecast in forecasts:
        forecast_list.append({
            "dt": int(forecast.datetime.timestamp()),
            "main": {
                "temp": forecast.temp,
                "feels_like": forecast.feels_like,
                "temp_min": forecast.temp_min,
                "temp_max": forecast.temp_max,
                "pressure": forecast.pressure,
                "humidity": forecast.humidity,
            },
            "weather": [
                {
                    "main": forecast.weather_main,
                    "description": forecast.weather_description,
                    "icon": forecast.icon
                }
            ],
            "clouds": {
                "all": forecast.clouds
            },
            "wind": {
                "speed": forecast.wind_speed,
                "deg": forecast.wind_deg
            },
            "visibility": forecast.visibility,
            "pop": forecast.pop,
            "rain": {
                "3h": forecast.rain_3h
            } if forecast.rain_3h is not None else {},
            "dt_txt": forecast.datetime.strftime("%Y-%m-%d %H:%M:%S")
        })

    return {
        "cod": "200",
        "message": 0,
        "cnt": len(forecast_list),
        "list": forecast_list,
        "city": {
            "id": location.id,
            "name": location.name,
            "coord": {
                "lat": location.point.y,
                "lon": location.point.x
            },
            "country": "IN"
        }
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
        return response.json()
        
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def fetch_forecast_data(lon, lat):
    """
    Fetch forecast data from OpenWeatherMap for the given location and save it.
    """
    api_key = settings.WEATHER_API_KEY
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch forecast: {response.status_code}")
        return

    return response.json()

