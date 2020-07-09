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

import datetime

from django.contrib import admin
from django.http import HttpResponse
from django.urls import path


def get_page_goodbye(request):
    hour = datetime.datetime.now().hour

    if hour in range(6, 11):
        msg = f"\n\t\t\t\t   Good morning!"
    elif hour in range(12, 24):
        msg = f"\n\t\t\t\t   Good day!"
    else:
        msg = f"\n\t\t\t\t   Good night!"

    return HttpResponse(msg)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('goodbye/', get_page_goodbye)
]
