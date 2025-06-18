from django.shortcuts import render, redirect, get_object_or_404
from .models import Location, WeatherForecast
from .utils import fetch_and_store_forecast, get_current_weather

def weathermap(request):
    return render(request, 'mainapp/weathermap.html')

def locations(request):
    locations = Location.objects.filter(user=request.user)
    locations_count = locations.count()
    context = {
        'locations': locations,
        'locations_count':locations_count,
        }
    return render(request, 'mainapp/locations.html', context)

def location_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        location = Location.objects.create(user=request.user, name=name, point=f'POINT({longitude} {latitude})')
        fetch_and_store_forecast(latitude, longitude, location)
        return redirect('locations')
    return render(request, 'mainapp/add_location.html')

def delete_location(request, location_id):
    location = get_object_or_404(Location, id=location_id, user=request.user)
    location.delete()
    return redirect('locations')

def get_location(request, location_id):
    location = get_object_or_404(Location, id=location_id, user=request.user)
    lat, lon = location.point.x, location.point.y
    current_data = get_current_weather(lat, lon)
    print(current_data)
    forecast_data = WeatherForecast.objects.filter(location=location)
    context = {
        'location':location,
        'lat': lat,
        'lon': lon,
        'current_data': current_data,
        'forecast_data':forecast_data,
    }
    return render(request, 'mainapp/location_detail.html', context)