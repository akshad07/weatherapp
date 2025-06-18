from django.urls import path, include
from .views import *

urlpatterns = [
    path('weathermap/', weathermap, name='weathermap'),  
    path('locations/', locations, name='locations'),
    path('locations/add_location/', location_add, name='add_location'),
    path('locations/delete_location/<uuid:location_id>/', delete_location, name='delete_location'),
    path('locations/detail/<uuid:location_id>/', get_location, name='get_location'),
    
]
