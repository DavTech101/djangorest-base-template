from . import views
from django.urls import path

urlpatterns = [
    path("products/", views.product_list, name="product-list"),
    path("products/<int:pk>/", views.product_detail),
    path("collections/", views.collection_list, name="collection-list"),
    path("collections/<int:pk>/", views.collection_detail, name="collection-detail"),
]
