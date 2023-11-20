from django.contrib.auth import login, authenticate
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages

from worker.tasks import send_mail_func
from worker.signals import user_signed_up_signal

from .forms import CustomUserCreationForm
from .serializers import RegisterSerializer, UserSerializer

from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer

def find_token_by_user_id(user_id):
    
    try:
        return Token.objects.get(user_id=user_id)
    except Token.DoesNotExist:
        return None
    
def find_user_by_id(id):
    
    try:
        return User.objects.get(pk=id)
    except User.DoesNotExist:
        return None

def find_user_by_name(name):
    
    try:
        return User.objects.get(username=name)
    except User.DoesNotExist:
        return None
    
def find_user_by_email(email):
    
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None


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
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # print(user)  
            send_mail_func(form.data)
            user_signed_up_signal.send(sender=None, user=user)
            login(request, user)
            return redirect(reverse("dashboard"))            
        return HttpResponseNotFound("Invalid Information")
    
#Class based view to register user
class RegisterUserAPIView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    
    def post(self, request, *args, **kwargs):
        if find_user_by_name(request.data['username']):
            return Response(
                    {"message": f"User with name {request.data['username']} already exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        if find_user_by_email(request.data['email']):
            return Response(
                    {"message": f"User with email {request.data['email']} already exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )  
        
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    
class AuthTokenAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = AuthTokenSerializer
    queryset = User.objects.all()
    
    def get(self, request, *args, **kwargs):
        
        user_id = request.user.id
        token = find_token_by_user_id(user_id)
        
        if token:
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        
        return Response(
                {"message": "Token had not created yet."},
                status=status.HTTP_404_NOT_FOUND
            )
        
    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']
        # print(username)
        # print(password)        
        user = find_user_by_name(username)
        if user.is_active:  
            authuser = authenticate(username=username, password=password)
            if authuser is not None:
                token, created = Token.objects.get_or_create(user=authuser)
                return Response(
                        {'token': token.key},
                        status=status.HTTP_201_CREATED
                    )
            
            else:
                
                return Response(
                        {'message': "Invalid username of password"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        
        else:            
            token, created = Token.objects.get_or_create(user=user)     
            # print("co active meo dau")       
            return Response(
                    {'token': token.key},
                    status=status.HTTP_201_CREATED
                )
        
def activate(request, authtoken):
    
    try:
        user = Token.objects.get(key=authtoken).user
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None:
        user.is_active = True
        user.save()
        
        return redirect(reverse("login"))
    else:
    
        return redirect(reverse("dashboard"))  