from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from rest_framework.authtoken.models import Token

from .models import MyUser
from .forms import CustomUserCreationForm

# Register your models here.


# Display the custom field and make them editable through admin

class MyUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = MyUser
    list_display = ['username','email','is_staff', 'is_active']


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Token)
