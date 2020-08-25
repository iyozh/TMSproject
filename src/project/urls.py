"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import include, path, re_path

from utils.file_utils import css_handler, img_handler
from utils.theme_utils import NightModeView

urlpatterns = [
    path("", include("applications.main_page.urls")),
    path("admin/", admin.site.urls),
    path("goodbye/", include("applications.goodbye.urls")),
    path("resume/", include("applications.resume.urls")),
    path("projects/", include("applications.projects.urls")),
    path("hello/", include("applications.hello.urls")),
    path("stats/", include("applications.stats.urls")),
    path("education/", include("applications.education.urls")),
    path("test_projects/", include("applications.test_projects.urls")),
    path("blog/", include("applications.blog.urls")),
    re_path("img/(?P<path_to_file>.+)$", img_handler),
    re_path("css/(?P<path_to_file>.+)$", css_handler),
    re_path(".*night_mode", NightModeView.as_view(), name="night_mode"),

]
