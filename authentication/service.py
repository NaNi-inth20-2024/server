from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken


class AuthService:
    """
    Service class for handling authentication related operations.
    """

    def header_to_user(self, headers):
        """
        Extracts the user from the JWT token obtained from the request headers.
        :param headers: Dictionary containing request headers.
        :return: The user object if authentication is successful, None otherwise.
        """
        try:
            auth_header = headers.get(b'authorization', b'').decode('utf-8')
            jwt_token = auth_header.split()[1]
            return self.token_to_user(jwt_token)
        except Exception:
            return None

    def token_to_user(self, token):
        try:
            access_token = AccessToken(token)
            user_payload = access_token.payload
            id = user_payload.get('user_id')
            return User.objects.get(pk=id)
        except:
            return None


auth_service = AuthService()
