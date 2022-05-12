from . import views
from django.urls import path

urlpatterns = [
    path("products/", views.product_list, name="index"),
    path("products/<int:pk>/", views.product_detail, name="index"),
]
