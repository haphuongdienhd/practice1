import datetime
import pytz

from django.contrib.auth import authenticate

from user.models import MyUser

from .serializers import RegisterSerializer, UserSerializer

from ..services import (
    find_token_by_user_id,
    find_user_by_email,
    find_user_by_name,
)

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer


#Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    queryset = MyUser.objects.all()
    
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
    serializer_class = AuthTokenSerializer
    queryset = MyUser.objects.all()
    
    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        token = find_token_by_user_id(user_id)
        if user_id:
            if token:
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            
            return Response(
                    {"message": "Token had not created yet."},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(
                    {"message": "UNAUTHORIZED."},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        
    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']
        user = find_user_by_name(username)
        if user.is_active:  
            authuser = authenticate(username=username, password=password)
            if authuser is not None:
                token, created = Token.objects.get_or_create(user=authuser)
                if not created:
                # update the created time of the token to keep it valid
                    token.created = datetime.datetime.utcnow()
                    token.save()
                return Response(
                        {'token': token.key,
                         'created': token.created},
                        status=status.HTTP_201_CREATED
                    )
            
            else:
                
                return Response(
                        {'message': "Invalid username of password"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        
        else:            
            token, created = Token.objects.get_or_create(user=user)
            if not created:
                # update the created time of the token to keep it valid
                token.created = datetime.datetime.utcnow()
                token.save()
            # print("co active meo dau")       
            return Response(
                    {'token': token.key},
                    status=status.HTTP_201_CREATED
                )