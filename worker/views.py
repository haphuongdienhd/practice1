from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth import login
from django.urls import reverse
from django_celery_beat.models import PeriodicTask,CrontabSchedule

from .tasks import fun, send_mail_func
from .forms import CustomUserCreationForm
from .signals import user_signed_up_signal

# Create your views here.

def testView(request):
    fun.delay()
    return HttpResponse("Done")