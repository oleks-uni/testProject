import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()

class JWTAuth(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith(settings.SIMPLE_JWT['AUTH_HEADER_TYPES'][0]):
            return None
        
        token = auth_header.split()[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            user = User.objects.get(id=user_id)
            return (user, token)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed({
                'error': 'token_expired_error',
                'message': 'Token expired',
                })
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')

def generate_jwt_token(user):
    token_payload = {
        'user_id': user.id,
        'exp': datetime.now(timezone.utc) + timedelta(minutes=3),
        'iat': datetime.now(timezone.utc)
    }

    access_payload = token_payload.copy()
    refresh_paload =  token_payload.copy()
    refresh_paload['exp'] =  datetime.now(timezone.utc) + timedelta(days=3)
    
    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm='HS256')
    refresh_token = jwt.encode(refresh_paload, settings.SECRET_KEY, algorithm='HS256')

    return {
        'access': access_token,
        'refresh': refresh_token
    }