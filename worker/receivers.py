from django.dispatch import receiver

from user.models import MyUser
from user.signals import user_signed_up_signal

from .tasks import send_mail_func


@receiver(user_signed_up_signal)
def confirm_signup(sender, data, **kwargs):
    print(send_mail_func.apply_async((data,), countdown=2))
    print('You have signed up successfully')
    print('sender', sender())