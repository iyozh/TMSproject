from django.urls import path

from applications.resume.apps import ResumeConfig
from applications.resume.views import ResumeView

app_name = ResumeConfig.label

urlpatterns = [path("", ResumeView.as_view(), name="resume")]
