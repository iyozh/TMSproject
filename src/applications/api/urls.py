from django.urls import include, path
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path("", include("applications.api.impl.urls")),
    path("obtain_auth_token/", ObtainAuthToken.as_view(), name="obtain_auth_token"),
]
