from django.urls import path

from applications.main_page.views import MainPageView

from .apps import MainPageConfig

app_name = MainPageConfig.label

urlpatterns = [
    path("", MainPageView.as_view(), name="main"),
    path("night_mode", MainPageView.as_view(), name="night_mode"),
]
