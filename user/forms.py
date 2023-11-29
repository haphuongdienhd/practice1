from django.contrib.auth.forms import UserCreationForm

from user.models import MyUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = MyUser
        fields = UserCreationForm.Meta.fields + ("email",)