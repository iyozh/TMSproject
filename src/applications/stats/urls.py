from django.urls import path

from .apps import StatsConfig
from .views import get_stats

app_name = StatsConfig.label

urlpatterns = [
    path("", get_stats,name = "statistic")
]