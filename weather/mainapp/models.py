from django.db import models
import uuid
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models as gismodel

User = get_user_model()

class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="locations")
    name = models.CharField(max_length=255)
    point = gismodel.PointField(srid=4326)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"
    
class WeatherForecast(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="weather_forecasts")
    datetime = models.DateTimeField(null=True, blank=True)    
    temp = models.FloatField(null=True, blank=True)
    feels_like = models.FloatField(null=True, blank=True)
    temp_min = models.FloatField(null=True, blank=True)
    temp_max = models.FloatField(null=True, blank=True)
    humidity = models.IntegerField(null=True, blank=True)
    pressure = models.IntegerField(null=True, blank=True)
    weather_main = models.CharField(max_length=50, null=True, blank=True)
    weather_description = models.CharField(max_length=100, null=True, blank=True)
    icon = models.CharField(max_length=10, null=True, blank=True)
    clouds = models.IntegerField(null=True, blank=True)
    wind_speed = models.FloatField(null=True, blank=True)
    wind_deg = models.IntegerField(null=True, blank=True)    
    visibility = models.IntegerField(null=True, blank=True)
    pop = models.FloatField(null=True, blank=True) 
    rain_3h = models.FloatField(null=True, blank=True)  

    def __str__(self):
        return f"{self.datetime} - {self.weather_main or 'Unknown'} ({self.temp or 'N/A'}°C)"



