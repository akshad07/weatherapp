from django.shortcuts import render, redirect, get_object_or_404
from .models import Location, WeatherForecast
from .utils import fetch_and_store_forecast, get_current_weather, format_forecast_response, get_current_weather_data,fetch_forecast_data
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import LocationSerializer
from .authentication import APIKeyAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .swagger import *

def weathermap(request):
    """Render the weather map page.
    Used for displaying weather overlays and visualizations."""
    return render(request, 'mainapp/weathermap.html')

@login_required
def locations(request):
    """List all saved locations for the current user.
    Also includes a count of total locations."""
    locations = Location.objects.filter(user=request.user)
    locations_count = locations.count()
    context = {
        'locations': locations,
        'locations_count': locations_count,
    }
    return render(request, 'mainapp/locations.html', context)

@login_required
def location_add(request):
    """Handle form to add a new location with coordinates.
    On submit, saves the location and fetches weather forecast."""
    if request.method == 'POST':
        name = request.POST.get('name')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        location = Location.objects.create(user=request.user, name=name, point=f'POINT({longitude} {latitude})')
        fetch_and_store_forecast(latitude, longitude, location)
        return redirect('locations')
    return render(request, 'mainapp/add_location.html')

@login_required
def delete_location(request, location_id):
    """Delete a saved location belonging to the user.
    Redirects to the locations list after deletion."""
    location = get_object_or_404(Location, id=location_id, user=request.user)
    location.delete()
    return redirect('locations')

@login_required
def get_location(request, location_id):
    """Show current and forecast weather for a specific location.
    Fetches live weather data and forecasts from the database."""
    location = get_object_or_404(Location, id=location_id, user=request.user)
    lat, lon = location.point.x, location.point.y
    current_data = get_current_weather(lat, lon)
    forecast_data = WeatherForecast.objects.filter(location=location)
    context = {
        'location': location,
        'lat': lat,
        'lon': lon,
        'current_data': current_data,
        'forecast_data': forecast_data,
    }
    return render(request, 'mainapp/location_detail.html', context)


#_________________APIENDPOINTS_____________________#


class LocationAPIView(APIView):
    authentication_classes = [APIKeyAuthentication]

    @swagger_auto_schema(
        operation_description="""
        Get all geometries for the authenticated user in GeoJSON format.
        
        Authentication:
        - Required: Yes
        - Type: API Key
        - Header: X-API-Key
        - Format: UUID
        """,
        manual_parameters=[x_api_key_header],
        responses={
            200: location_list,
            400: 'Bad Request',
            401: 'Unauthorized',
            403: 'Forbidden',
            500: 'Internal Server Error'
        },
        security=api_key_security
    )
    def get(self, request):
        """Get all locations for the authenticated user."""
        locations = Location.objects.filter(user=request.user)
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="""
        Create a new location with name and geometry.
        
        Authentication:
        - Required: Yes
        - Type: API Key
        - Header: X-API-Key
        - Format: UUID
        """,
        manual_parameters=[x_api_key_header],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name', 'geojson'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the Location'),
                'geojson': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description='Location in GeoJSON format',
                    properties={
                        'type': openapi.Schema(type=openapi.TYPE_STRING, description='GeoJSON type (e.g., Point)'),
                        'coordinates': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_NUMBER),
                            description='Coordinate array'
                        )
                    }
                )
            }
        ),
        responses={
            201: openapi.Response(
                description='Location created successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID),
                        'name': openapi.Schema(type=openapi.TYPE_STRING),
                        'point': openapi.Schema(type=openapi.TYPE_OBJECT),
                        'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
                    }
                )
            ),
            400: 'Bad Request',
            401: 'Unauthorized',
            403: 'Forbidden',
            500: 'Internal Server Error'
        },
        security=api_key_security
    )
    def post(self, request):
        """Create a location with name and GeoJSON."""
        serializer = LocationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            location = serializer.instance
            latitude =  location.point.y
            longitude = location.point.x
            fetch_and_store_forecast(latitude, longitude, location)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="""
        Delete a location by ID.

        Authentication:
        - Required: Yes
        - Type: API Key
        - Header: X-API-Key
        - Format: UUID

        Query Parameters:
        - `id` (UUID): The ID of the location to delete.
        """,
        manual_parameters=[
            x_api_key_header,
            location_id
        ],
        responses={
            204: openapi.Response(description='Location deleted successfully'),
            400: 'Bad Request',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        security=api_key_security
    )
    def delete(self, request):
        """Delete a location by ID (?id=<uuid>)."""
        location_id = request.query_params.get('id')
        if not location_id:
            return Response({"detail": "Location ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        location = get_object_or_404(Location, id=location_id, user=request.user)
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LocationCurrentWeatherAPI(APIView):
    authentication_classes = [APIKeyAuthentication]

    @swagger_auto_schema(
        operation_description="Get current weather for a location by ID.",
        manual_parameters=[x_api_key_header,location_id],
        responses={
            200: CurrentWeatherSchema,
            400: 'Bad Request',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not Found',
            500: 'Internal Server Error'
        },   
    )
    def get(self, request):
        """Get current weather for a specific location."""
        location_id = request.query_params.get('id')
        location = get_object_or_404(Location, id=location_id, user=request.user)
        lat, lon = location.point.x, location.point.y
        current_data = get_current_weather_data(lat, lon)
        if not current_data:
            return Response({"detail": "Could not fetch current weather data."}, status=status.HTTP_404_NOT_FOUND)
        return Response(current_data, status=status.HTTP_200_OK)
    

class LocationForecastWeatherAPI(APIView):
    authentication_classes = [APIKeyAuthentication]

    @swagger_auto_schema(
        operation_description="Get weather forecast for a location by ID.",
        manual_parameters=[x_api_key_header,location_id],
        responses={
            200: ForecastWeatherSchema,
            400: 'Bad Request',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
    )

    def get(self, request):
        location_id = request.query_params.get('id')
        location = get_object_or_404(Location, id=location_id, user=request.user)
        forecasts = WeatherForecast.objects.filter(location=location)

        if not forecasts.exists():
            return Response({"detail": "Could not fetch weather forecast data."}, status=status.HTTP_404_NOT_FOUND)

        response_data = format_forecast_response(location, forecasts)
        return Response(response_data, status=status.HTTP_200_OK)
    

class PublicCurrentWeatherAPI(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Get current weather for a specific latitude and longitude.",
        manual_parameters=[lat_param, lon_param],
        responses={
            200: CurrentWeatherSchema,
            400: 'Bad Request',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not Found',
            500: 'Internal Server Error'
        }
    )
    def get(self, request):
        """Get current weather for a specific latitude and longitude."""
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')

        if not latitude or not longitude:
            return Response({"detail": "Latitude and longitude are required."}, status=status.HTTP_400_BAD_REQUEST)

        current_data = get_current_weather_data(longitude, latitude)
        if not current_data:
            return Response({"detail": "Could not fetch current weather data."}, status=status.HTTP_404_NOT_FOUND)

        return Response(current_data, status=status.HTTP_200_OK)

class PublicForecastWeatherAPI(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Get weather forecast for a specific latitude and longitude.",
        manual_parameters=[lat_param, lon_param],
        responses={
            200: ForecastWeatherSchema,
            400: 'Bad Request',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not Found',
            500: 'Internal Server Error'
        }
    )
    def get(self, request):
        """Get weather forecast for a specific latitude and longitude."""
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')

        if not latitude or not longitude:
            return Response({"detail": "Latitude and longitude are required."}, status=status.HTTP_400_BAD_REQUEST)

        forecasts = fetch_forecast_data(longitude, latitude)
        if not forecasts:
            return Response({"detail": "Could not fetch weather forecast data."}, status=status.HTTP_404_NOT_FOUND)

        return Response(forecasts, status=status.HTTP_200_OK)