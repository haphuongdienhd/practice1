import datetime
import pytz

from django.conf import settings
from django.utils import timezone
from user.models import MyUser

from rest_framework.authtoken.models import Token

# from user.models import MyUser

def find_token_by_user_id(user_id):
    
    try:
        return Token.objects.get(user_id=user_id)
    except Token.DoesNotExist:
        return None
    
def find_user_by_id(id):
    
    try:
        return MyUser.objects.get(pk=id)
    except MyUser.DoesNotExist:
        return None

def find_user_by_name(name):
    
    try:
        return MyUser.objects.select_related().get(username=name)
    except MyUser.DoesNotExist:
        return None
    
def find_user_by_email(email):
    
    try:
        return MyUser.objects.get(email=email)
    except MyUser.DoesNotExist:
        return None

def token_expire(token_created):
    """Return True if Token has not been expired
    Else return False"""
    utc_now = timezone.now()
    utc_now = utc_now.replace(tzinfo=pytz.utc)

    if token_created < utc_now - settings.AUTH_TOKEN_VALIDITY:
        return False
    
    return True
