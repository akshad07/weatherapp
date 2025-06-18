from django.contrib import admin
from .models import Location, WeatherForecast

admin.site.register(Location)
admin.site.register(WeatherForecast)