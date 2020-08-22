from django.urls import path

from applications.hello.apps import HelloConfig
from applications.hello.views import HelloView

app_name = HelloConfig.label

urlpatterns = [
    path("", HelloView.as_view(), name="hello"),
]
