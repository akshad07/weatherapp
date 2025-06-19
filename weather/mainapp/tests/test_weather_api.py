from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from uuid import uuid4

from mainapp.models import Location
from accounts.models import Profile  

User = get_user_model()


class WeatherAPITest(APITestCase):
    def setUp(self):        
        self.user, _ = User.objects.get_or_create(email='user@example.com')
        self.user.set_password('password')
        self.user.save()

        self.api_key_profile, _ = Profile.objects.get_or_create(user=self.user)
        
        # Ensure the profile has a valid key (assuming your Profile model has a `key` field)
        if not self.api_key_profile.api_key:
            from uuid import uuid4
            self.api_key_profile.api_key = uuid4()
            self.api_key_profile.save()

        self.client = APIClient()
        self.auth_header = {'HTTP_X_API_KEY': str(self.api_key_profile.api_key)}

        self.location = Location.objects.create(
            user=self.user,
            name="Test Location",
            point="POINT(77.5946 12.9716)"  # Example coordinates (longitude latitude)
        )


    def test_authenticated_location_get(self):
        url = reverse('location-api')
        response = self.client.get(url, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_location_post(self):
        url = reverse('location-api')
        payload = {
            'name': 'Test Location POST',
            'geojson': {
                'type': 'Point',
                'coordinates': [77.5946, 12.9716],
            }
        }
        response = self.client.post(url, data=payload, format='json', **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_authenticated_location_delete(self):
        url = reverse('location-api') + f'?id={self.location.id}'
        response = self.client.delete(url, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_current_weather_authenticated(self):
        url = reverse('weather-current-api') + f'?id={self.location.id}'
        response = self.client.get(url, **self.auth_header)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])  # External fetch can fail

    def test_forecast_weather_authenticated(self):
        url = reverse('weather-forecast-api') + f'?id={self.location.id}'
        response = self.client.get(url, **self.auth_header)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])

    def test_public_current_weather(self):
        url = reverse('public-current-api') + '?latitude=12.9716&longitude=77.5946'
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])

    def test_public_forecast_weather(self):
        url = reverse('public-forecast-api') + '?latitude=12.9716&longitude=77.5946'
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])

    def test_missing_api_key(self):
        url = reverse('location-api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_delete_id(self):
        url = reverse('location-api') + f'?id={uuid4()}'
        response = self.client.delete(url, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
