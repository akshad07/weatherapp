from celery import shared_task
from concurrent.futures import ThreadPoolExecutor, as_completed
from .models import Location, WeatherForecast
from .utils import fetch_and_store_forecast

@shared_task(time_limit=43200, soft_time_limit=43200)
def weather_celery():
    """
    Celery task to fetch and store weather forecast for all locations using multithreading.
    """
    locations = Location.objects.all()

    def process_location(location):
        try:
            WeatherForecast.objects.filter(location=location).delete()
            lat = location.point.y
            lon = location.point.x
            fetch_and_store_forecast(lat, lon, location)
        except Exception as e:
            print(f"Error processing location {location.id}: {str(e)}")

    max_threads = min(10, len(locations))

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(process_location, loc) for loc in locations]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Thread raised an exception: {str(e)}")

