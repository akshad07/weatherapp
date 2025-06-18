from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from accounts.models import Profile
import uuid

class APIKeyAuthentication(BaseAuthentication):
    """
    Custom authentication using X-API-Key header for Profile-based API key access.
    """

    def authenticate(self, request):
        api_key_header = request.headers.get('X-API-Key')  # Better than META

        if not api_key_header:
            return None  # No key provided; skip to next auth class

        try:
            api_key_uuid = uuid.UUID(api_key_header)
        except ValueError:
            raise AuthenticationFailed('Invalid API key format')

        try:
            user = Profile.objects.get(api_key=api_key_uuid).user
            return (user, None)
        except Profile.DoesNotExist:
            raise AuthenticationFailed('Invalid API key')

    def authenticate_header(self, request):
        return 'X-API-Key'
