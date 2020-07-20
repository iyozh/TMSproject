from django.urls import path
from .apps import MainPageConfig
from applications.main_page.views import MainPageView

app_name = MainPageConfig.label

urlpatterns = [
    path("", MainPageView.as_view(), name="main")
]