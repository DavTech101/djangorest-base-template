from decimal import Decimal
from rest_framework import serializers
from .models import Product, Customer, Collection, Review


class CollectionSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)

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
    class Meta:
        model = Customer
        fields = ("id", "first_name", "last_name", "email", "phone", "birth_date")


class ReviewSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        product = Product.objects.get(pk=self.context["product_id"])
        return Review.objects.create(product=product, **validated_data)

    class Meta:
        model = Review
        fields = ("id", "author", "review", "created_at")
