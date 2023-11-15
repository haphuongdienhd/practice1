from django.urls import include, re_path, path
from .views import dashboard, register
from .views import RegisterUserAPIView, AuthTokenAPIView
from django.views.generic import RedirectView


urlpatterns = [
    re_path(r"^account/", include("django.contrib.auth.urls")),
    path('', RedirectView.as_view(url='dashboard/')),
    path("dashboard/", dashboard, name="dashboard"),
    re_path(r"^register/", register, name="register"),
    path('api/registors/',RegisterUserAPIView.as_view(), name="api_register"),    
    path('api/api-auth/', include('rest_framework.urls'), name="session_login"),
    path('api/auth-tokens/',AuthTokenAPIView.as_view(), name="api_token"),
]