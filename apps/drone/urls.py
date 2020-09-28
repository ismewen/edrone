from django.urls import path
from . import views
from .views import EdroneAPIView
urlpatterns = [
    path('hello_world/', views.hello_world),
    path('edrone/', EdroneAPIView.as_view()),
]
