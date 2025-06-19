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

ForecastWeatherSchema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "cod": openapi.Schema(type=openapi.TYPE_STRING),
        "message": openapi.Schema(type=openapi.TYPE_INTEGER),
        "cnt": openapi.Schema(type=openapi.TYPE_INTEGER),
        "list": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "dt": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "main": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "temp": openapi.Schema(type=openapi.TYPE_NUMBER),
                            "feels_like": openapi.Schema(type=openapi.TYPE_NUMBER),
                            "temp_min": openapi.Schema(type=openapi.TYPE_NUMBER),
                            "temp_max": openapi.Schema(type=openapi.TYPE_NUMBER),
                            "pressure": openapi.Schema(type=openapi.TYPE_INTEGER),
                            "humidity": openapi.Schema(type=openapi.TYPE_INTEGER),
                        },
                    ),
                    "weather": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "main": openapi.Schema(type=openapi.TYPE_STRING),
                                "description": openapi.Schema(type=openapi.TYPE_STRING),
                                "icon": openapi.Schema(type=openapi.TYPE_STRING),
                            }
                        ),
                    ),
                    "clouds": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={"all": openapi.Schema(type=openapi.TYPE_INTEGER)},
                    ),
                    "wind": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "speed": openapi.Schema(type=openapi.TYPE_NUMBER),
                            "deg": openapi.Schema(type=openapi.TYPE_INTEGER),
                        },
                    ),
                    "visibility": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "pop": openapi.Schema(type=openapi.TYPE_NUMBER),
                    "rain": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={"3h": openapi.Schema(type=openapi.TYPE_NUMBER)},
                    ),
                    "dt_txt": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
        ),
        "city": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "name": openapi.Schema(type=openapi.TYPE_STRING),
                "coord": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "lat": openapi.Schema(type=openapi.TYPE_NUMBER),
                        "lon": openapi.Schema(type=openapi.TYPE_NUMBER),
                    },
                ),
                "country": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    },
)

from drf_yasg import openapi

CurrentWeatherSchema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "coord": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "lon": openapi.Schema(type=openapi.TYPE_NUMBER),
                "lat": openapi.Schema(type=openapi.TYPE_NUMBER),
            }
        ),
        "weather": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "main": openapi.Schema(type=openapi.TYPE_STRING),
                    "description": openapi.Schema(type=openapi.TYPE_STRING),
                    "icon": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
        ),
        "base": openapi.Schema(type=openapi.TYPE_STRING),
        "main": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "temp": openapi.Schema(type=openapi.TYPE_NUMBER),
                "feels_like": openapi.Schema(type=openapi.TYPE_NUMBER),
                "temp_min": openapi.Schema(type=openapi.TYPE_NUMBER),
                "temp_max": openapi.Schema(type=openapi.TYPE_NUMBER),
                "pressure": openapi.Schema(type=openapi.TYPE_INTEGER),
                "humidity": openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
        "visibility": openapi.Schema(type=openapi.TYPE_INTEGER),
        "wind": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "speed": openapi.Schema(type=openapi.TYPE_NUMBER),
                "deg": openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
        "clouds": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "all": openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
        "dt": openapi.Schema(type=openapi.TYPE_INTEGER),
        "sys": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "type": openapi.Schema(type=openapi.TYPE_INTEGER),
                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "country": openapi.Schema(type=openapi.TYPE_STRING),
                "sunrise": openapi.Schema(type=openapi.TYPE_INTEGER),
                "sunset": openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
        "timezone": openapi.Schema(type=openapi.TYPE_INTEGER),
        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
        "name": openapi.Schema(type=openapi.TYPE_STRING),
        "cod": openapi.Schema(type=openapi.TYPE_INTEGER),
    },
)

# Security declaration (optional but useful)
api_key_security = [{'X-API-Key': []}]

# Aliases for OpenAPI Types
OpenAPIType = openapi.TYPE_OBJECT
OpenAPIFormat = openapi.FORMAT_DATE
