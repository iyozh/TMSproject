from django.urls import path

from applications.goodbye.views import GoodbyeView

from .apps import GoodbyeConfig

app_name = GoodbyeConfig.label

urlpatterns = [path("", GoodbyeView.as_view(), name="greeting")]
