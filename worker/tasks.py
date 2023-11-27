import datetime
import secrets

from django.utils import timezone
from django.db import connection
from django.core.mail import send_mail

from celery import shared_task

from practice1 import settings
from user.models import MyUser
from user.services import find_user_by_name

BASE_URL = 'http://127.0.0.1:8000'

@shared_task(bind=True)
def fun(self):
    # operations
    print("You are in Fun function")
    return "done"

@shared_task(bind=True)
def send_mail_func(self, username):
    user = find_user_by_name(username)
    make_hash_token(user)
    mail_subject="Sign up"
    message=f"""HELLO!!!...\n
    Hi user {user},\n
    Please click in {BASE_URL + '/activate/' + str(user.signup_token)} to activate your account.\n
    """
    to_email=user.email
    send_mail(
        subject=mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=True,
        )
    
    return "Task Successfull"

def make_hash_token(user):
    user.signup_token = secrets.token_urlsafe(16)
    user.signup_token_created = datetime.datetime.utcnow()
    user.save()


@shared_task(bind=True)
def send_mail_to_admins_func(self):
    """Email for all Admins list Users signed up today"""
    users = MyUser.objects.filter(is_staff=True)
    # User has date_joined default timezone.now
    # Solution: list all user has date_joined greater equal than today at 00:00:00
    today = timezone.now().replace(hour=0,minute=0,second=0,microsecond=0)
    user_signed_up = MyUser.objects.filter(date_joined__gte=today)
    for user in users:
        mail_subject="List users sign up today"
        message="List users sign up today:\n"
        for usu in user_signed_up:
            message += f"""username: {usu.username}, email: {usu.email}, had signed up at: {usu.date_joined} \n"""
        to_email=user.email
        send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,
            )
    return "Task Successfull"



def send_mail_hc_fail(self):
    users = MyUser.objects.filter(is_staff=True)
    for user in users:
        mail_subject="Health check fail"
        message="Health check fail\n"
        to_email=user.email
        send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,
            )


@shared_task(bind=True)
def health_check_per_minute(self):
    print("health_check_per_minute")
    with connection.cursor() as cursor:
        cursor.execute("select 1")
        one = cursor.fetchone()[0]
        if one != 1:
            send_mail_hc_fail()
            return "Health Failed"
    return "Health Successful"