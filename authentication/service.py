from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken


class AuthService:
    def token_to_user(self, headers):
        try:
            auth_header = headers.get(b'authorization', b'').decode('utf-8')
            jwt_token = auth_header.split()[1]
            access_token = AccessToken(jwt_token)
            user_payload = access_token.payload
            id = user_payload.get('user_id')
            return User.objects.get(pk=id)
        except Exception:
            return None


auth_service = AuthService()
