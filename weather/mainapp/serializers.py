from rest_framework import serializers
from .models import Location
from django.contrib.gis.geos import GEOSGeometry, GEOSException

class LocationSerializer(serializers.ModelSerializer):
    geojson = serializers.JSONField(write_only=True)

    class Meta:
        model = Location
        fields = ['id', 'name', 'geojson', 'point', 'created_at']
        read_only_fields = ['id', 'point', 'created_at']

    def validate_geojson(self, value):
        try:
            geometry = GEOSGeometry(str(value), srid=4326)
            if geometry.geom_type != 'Point':
                raise serializers.ValidationError("Only Point geometries are allowed.")
            return geometry
        except (ValueError, GEOSException, TypeError):
            raise serializers.ValidationError("Invalid GeoJSON format.")

    def create(self, validated_data):
        point = validated_data.pop('geojson')  # Already validated as a GEOSGeometry Point
        validated_data['point'] = point
        validated_data['user'] = self.context['request'].user
        return Location.objects.create(**validated_data)
