from django.shortcuts import render, redirect
from .models import Location
from .utils import fetch_and_store_forecast

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
    location = Location.objects.get(id=location_id)
    location.delete()
    return redirect('locations')