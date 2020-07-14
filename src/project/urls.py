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
from django.urls import path

from pages.education import edu_handler
from pages.goodbye import get_page_goodbye
from pages.hello import handler_hello
from pages.projects import get_projects_page, get_projects_css
from pages.resume import get_portfolio, get_resume_css
from pages.stats import get_stats
from pages.test_projects import projects_handler, get_editing_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('goodbye/', get_page_goodbye),
    path('resume/', get_portfolio),
    path('projects/', get_projects_page),
    path('resume/portfolio/aboutme/css/main.css', get_resume_css),
    path('projects/portfolio/projects/css/main.css', get_projects_css),
    path('hello/', handler_hello),
    path('stats/', get_stats),
    path('education/', edu_handler),
    path('education/night_mode', edu_handler),
    path('test_projects/', projects_handler),
    path('test_projects/editing', get_editing_page),
    path('test_projects/editing/add', projects_handler),
    path('test_projects/editing/change', projects_handler),
    path('test_projects/editing/delete', projects_handler),

]
