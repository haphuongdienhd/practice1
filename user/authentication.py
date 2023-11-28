
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token

from .utils import token_expire


class ExpiringTokenAuthentication(TokenAuthentication):
    """
    Expiring token.
    It expires and requiring client to supply valid username 
    and password for new one to be created.
    """

    model = Token

    def authenticate_credentials(self, key, request=None):
        models = self.get_model()

        try:
            token = models.objects.select_related("user").get(key=key)
        except models.DoesNotExist:
            raise AuthenticationFailed(
                {"error": "Invalid or Inactive Token", "is_authenticated": False}
            )

        if not token.user.is_active:
            raise AuthenticationFailed(
                {"error": "Invalid user", "is_authenticated": False}
            )

        if not token_expire(token):
            raise AuthenticationFailed(
                {"error": "Token has expired", "is_authenticated": False}
            )
        return token.user, token