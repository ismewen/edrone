from django.urls import path

from .views import EdroneAPIView

urlpatterns = [
    path("edrone/", EdroneAPIView.as_view())
]
