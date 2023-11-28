from django.dispatch import receiver
from .signals import user_signed_up_signal


@receiver(user_signed_up_signal)
def confirm_signup(sender, **kwargs):
    print('You have signed up successfully')
    print('sender', sender)
