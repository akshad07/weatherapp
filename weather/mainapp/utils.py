import requests
from .models import WeatherForecast
from django.conf import settings


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


def get_current_weather(lat, lon):
    """
    Fetch and return formatted current weather data from OpenWeatherMap for given lat/lon.
    """
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

        # Extract & format key details
        return {
            "city": data.get("name"),
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
            "sunrise": data["sys"].get("sunrise"),
            "sunset": data["sys"].get("sunset"),
        }

    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
