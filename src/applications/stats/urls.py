from django.urls import path

from .apps import StatsConfig
from .views import Reset, StatsView

app_name = StatsConfig.label

urlpatterns = [
    path("", StatsView.as_view(), name="statistic"),
    path("reset", Reset.as_view(), name="reset"),
]
