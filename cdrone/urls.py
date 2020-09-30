"""cdrone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
import logging

from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include

from cdrone import discovery
from cdrone.core import router

logger = logging.getLogger("default")
discovery.auto_discovery()


def index(request):
    return HttpResponse("master")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('v1/', include(router.get_urls()))
]

urlpatterns += discovery.auto_get_urlpatterns()
