from rest_framework import status
from .models import Product, Collection, Customer, Order, OrderItem
from rest_framework.response import Response
from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from .serializers import ProductSerializer, CollectionSerializer


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count("products")).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs["pk"]).count() >= 1:
            return Response(
                {"error": "Collection cannot be deleted, it has products in it."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

        return super().destroy(request, *args, **kwargs)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs["pk"]).count() >= 1:
            return Response(
                {"error": "Product cannot be deleted, it is in an ordered item."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)
