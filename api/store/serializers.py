from rest_framework import serializers
from .models import Product, Customer, Collection


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    Title = serializers.CharField(max_length=255)
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2)
     
    class Meta:
        model = Product
