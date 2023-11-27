import datetime
import pytz

from django.contrib.auth import login
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.urls import reverse

from user.models import MyUser

from .forms import CustomUserCreationForm
from .services import token_expire
from .signals import user_signed_up_signal

def dashboard(request):
    
    return render(request, "user/dashboard.html")

def register(request):
    if request.method == "GET":
        return render(
            request, "user/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():                      
            userform = form.save()
            userform.is_active = False
            userform.save()
            user_signed_up_signal.send(sender=MyUser,data=userform.username)
            login(request, userform)
            return redirect(reverse("dashboard"))            
        return HttpResponseNotFound("Invalid Information")
    
            
def activate(request, signup_token):
    
    try:
        user = MyUser.objects.get(signup_token=signup_token)
    except(TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None
    if user is not None:        
        if not user.is_active:
            if not token_expire(user.signup_token_created):
                user.delete()
                return HttpResponseBadRequest("""<h1>Token had Expired, You must register again<h1>""")                
            user.is_active = True
            user.save()        
            return redirect(reverse("login"))
        
        else:
            return HttpResponseNotFound("<h1>User already active</h1>")            
        
    else:
        return HttpResponseNotFound("<h1>User not Found, have to sign up</h1>")