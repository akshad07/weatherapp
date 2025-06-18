from django.urls import path, include
from .views import *

urlpatterns = [
    path('weathermap/', weathermap, name='weathermap'),  
    path('locations/', locations, name='locations'),
    path('locations/add_location/', location_add, name='add_location'),
    path('locations/delete_location/<uuid:location_id>/', delete_location, name='delete_location'),
    path('locations/detail/<uuid:location_id>/', get_location, name='get_location'),
    path('api/location/', LocationAPIView.as_view(), name='location-api'),
    path('api/location/weather/current/', LocationCurrentWeatherAPI.as_view(), name='weather-current-api'),
    path('api/location/weather/forecast/', LocationForecastWeatherAPI.as_view(), name='weather-forecast-api'),

    path('api/public/weather/current/', PublicCurrentWeatherAPI.as_view(), name='public-current-api'),
    path('api/public/weather/forecast/', PublicForecastWeatherAPI.as_view(), name='public-forecast-api'),
]
