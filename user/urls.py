from django.urls import include, re_path, path
from django.views.generic import RedirectView

from .views import dashboard, register, activate
from user.api import urls as apiurls

urlpatterns = [
    re_path(r"^account/", include("django.contrib.auth.urls")),
    path('', RedirectView.as_view(url='dashboard/')),
    path("dashboard/", dashboard, name="dashboard"),
    re_path(r"^register/", register, name="register"),
    path('activate/<str:authtoken>', activate, name='activate_url'),
]

urlpatterns += apiurls.urlpatterns