from rest_framework import status
from .models import Product, Collection
from rest_framework.response import Response
from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from .serializers import ProductSerializer, CollectionSerializer
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
)


class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count=Count("products")).all()
    serializer_class = CollectionSerializer


class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(products_count=Count("products")).all()
    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() >= 1:
            return Response(
                {"error": "Collection cannot be deleted, it has products in it."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        collection.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related("collection").all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {"request": self.request}


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() >= 1:
            return Response(
                {"error": "Product cannot be deleted, it is in an ordered item."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
