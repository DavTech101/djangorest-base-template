from . import views
from django.urls import path

urlpatterns = [
    path("", views.say_hello, name="index"),
]
