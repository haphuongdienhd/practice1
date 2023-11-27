from django.urls import include, path
from .views import RegisterUserAPIView, AuthTokenAPIView


urlpatterns = [
    path('api/registors/',RegisterUserAPIView.as_view(), name="api_register"),    
    path('api/api-auth/', include('rest_framework.urls'), name="session_login"),
    path('api/auth-tokens/',AuthTokenAPIView.as_view(), name="api_token"),
]