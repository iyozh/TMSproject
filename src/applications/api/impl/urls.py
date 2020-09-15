from django.urls import include, path

urlpatterns = [path("v1/", include("applications.api.impl.v1.urls"))]
