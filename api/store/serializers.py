from decimal import Decimal
from rest_framework import serializers
from .models import Product, Customer, Collection


class CollectionSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField(method_name="get_products_count")

    def get_products_count(self, collection: Collection):
        return collection.products.count()

    class Meta:
        model = Collection
        fields = ("id", "title", "products_count")


class ProductSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")
    collection = serializers.HyperlinkedRelatedField(
        view_name="collection-detail",
        queryset=Collection.objects.all(),
    )

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)

    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "slug",
            "description",
            "unit_price",
            "price_with_tax",
            "collection",
        )


class CustomerSerializer(serializers.Serializer):
    pass
