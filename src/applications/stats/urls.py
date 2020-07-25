from django.urls import path

from .apps import StatsConfig
from .views import StatsView

app_name = StatsConfig.label

urlpatterns = [
    path("", StatsView.as_view(), name="statistic"),
    path("night_mode", StatsView.as_view(), name="night_mode"),
]
