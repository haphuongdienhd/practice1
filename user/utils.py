
import datetime
import pytz

from django.conf import settings
from django.utils import timezone


def token_expire(token):
    """Return True if Token has not been expired
    Else return False"""
    utc_now = timezone.now()
    utc_now = utc_now.replace(tzinfo=pytz.utc)

    if token.created < utc_now - settings.AUTH_TOKEN_VALIDITY:
        return False
    
    return True

