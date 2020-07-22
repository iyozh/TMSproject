from django.urls import path

from applications.education.apps import EducationConfig
from applications.education.views import EducationView

app_name = EducationConfig.label

urlpatterns = [
    path("", EducationView.as_view(), name="edu"),
    path("night_mode", EducationView.as_view(), name="night_mode")
]
