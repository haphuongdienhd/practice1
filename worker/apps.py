from django.apps import AppConfig


class WorkerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'worker'
    
    def ready(self):
        from .receivers import confirm_signup
        from .signals import user_signed_up_signal
        user_signed_up_signal.connect(confirm_signup)
