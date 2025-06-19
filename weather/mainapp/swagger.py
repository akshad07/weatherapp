from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Header param
x_api_key_header = openapi.Parameter(
    name='X-API-Key',
    in_=openapi.IN_HEADER,
    type=openapi.TYPE_STRING,
    required=True,
    description='Your API key (UUID format)'
)

location_id = openapi.Parameter(
                'id',
                openapi.IN_QUERY,
                description="UUID of the location to delete",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID,
                required=True
            )

lat_param = openapi.Parameter(
    name='latitude',
    in_=openapi.IN_QUERY,
    description="Latitude of the location eg: 20.00404270370521",
    type=openapi.TYPE_NUMBER,
    required=True
)

lon_param = openapi.Parameter(
    name='longitude',
    in_=openapi.IN_QUERY,
    description="Longitude of the location eg: 73.79459469473471",
    type=openapi.TYPE_NUMBER,
    required=True
)

location_list =openapi.Response(
                description='List of Locations',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'type': openapi.Schema(type=openapi.TYPE_STRING, description='FeatureCollection'),
                        'features': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'type': openapi.Schema(type=openapi.TYPE_STRING, description='Feature'),
                                    'geometry': openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        description='GeoJSON geometry'
                                    ),
                                    'properties': openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            'id': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID),
                                            'name': openapi.Schema(type=openapi.TYPE_STRING),
                                            'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time')
                                        }
                                    )
                                }
                            )
                        )
                    }
                )
)

from drf_yasg import openapi

ForecastWeatherSchema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "location": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "name": openapi.Schema(type=openapi.TYPE_STRING),
                "coordinates": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "lat": openapi.Schema(type=openapi.TYPE_NUMBER),
                        "lon": openapi.Schema(type=openapi.TYPE_NUMBER),
                    }
                )
            }
        ),
        "forecasts": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "timestamp": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "temperature": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "current": openapi.Schema(type=openapi.TYPE_NUMBER),
                            "min": openapi.Schema(type=openapi.TYPE_NUMBER),
                            "max": openapi.Schema(type=openapi.TYPE_NUMBER),
                        }
                    ),
                    "feels_like": openapi.Schema(type=openapi.TYPE_NUMBER),
                    "condition": openapi.Schema(type=openapi.TYPE_STRING),
                    "description": openapi.Schema(type=openapi.TYPE_STRING),
                    "humidity": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "wind": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "speed_kmh": openapi.Schema(type=openapi.TYPE_NUMBER),
                            "direction_deg": openapi.Schema(type=openapi.TYPE_INTEGER),
                        }
                    ),
                    "cloudiness_percent": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "rain_mm": openapi.Schema(type=openapi.TYPE_NUMBER),
                    "datetime": openapi.Schema(type=openapi.TYPE_STRING, format="date-time"),
                }
            )
        )
    }
)


CurrentWeatherSchema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "location": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "name": openapi.Schema(type=openapi.TYPE_STRING),
                "coordinates": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "lat": openapi.Schema(type=openapi.TYPE_NUMBER),
                        "lon": openapi.Schema(type=openapi.TYPE_NUMBER),
                    }
                ),
            }
        ),
        "weather": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "timestamp": openapi.Schema(type=openapi.TYPE_INTEGER),
                "temperature": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "current": openapi.Schema(type=openapi.TYPE_NUMBER),
                        "min": openapi.Schema(type=openapi.TYPE_NUMBER),
                        "max": openapi.Schema(type=openapi.TYPE_NUMBER),
                    }
                ),
                "feels_like": openapi.Schema(type=openapi.TYPE_NUMBER),
                "condition": openapi.Schema(type=openapi.TYPE_STRING),
                "description": openapi.Schema(type=openapi.TYPE_STRING),
                "humidity": openapi.Schema(type=openapi.TYPE_INTEGER),
                "wind": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "speed_kmh": openapi.Schema(type=openapi.TYPE_NUMBER),
                        "direction_deg": openapi.Schema(type=openapi.TYPE_INTEGER),
                    }
                ),
                "cloudiness_percent": openapi.Schema(type=openapi.TYPE_INTEGER),
                "rain_mm": openapi.Schema(type=openapi.TYPE_NUMBER),
                "datetime": openapi.Schema(type=openapi.TYPE_STRING, format="date-time"),
            }
        )
    }
)

# Security declaration (optional but useful)
api_key_security = [{'X-API-Key': []}]

# Aliases for OpenAPI Types
OpenAPIType = openapi.TYPE_OBJECT
OpenAPIFormat = openapi.FORMAT_DATE
