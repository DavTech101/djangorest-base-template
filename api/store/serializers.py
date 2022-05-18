from decimal import Decimal
from rest_framework import serializers
from .models import Product, Customer, Collection, Review, Cart, CartItem


########################### COLLECTION ###################################################
class CollectionSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Collection
        fields = ("id", "title", "products_count")


########################### PRODUCT ######################################################
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


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "title", "unit_price")


########################### CUSTOMER ###################################################
class CustomerSerializer(serializers.Serializer):
    class Meta:
        model = Customer
        fields = ("id", "first_name", "last_name", "email", "phone", "birth_date")


########################### CARTITEM ###################################################
class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(method_name="calculate_total_price")

    def calculate_total_price(self, cart_item: CartItem):
        return cart_item.product.unit_price * cart_item.quantity

    class Meta:
        model = CartItem
        fields = ("id", "product", "quantity", "total_price")


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_product_id(self, data):
        if not Product.objects.filter(pk=data).exists():
            raise serializers.ValidationError("Product does not exist.")

        return data

    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data
            )

        return self.instance

    class Meta:
        model = CartItem
        fields = ("id", "product_id", "quantity")


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ("quantity",)


########################### CART ######################################################
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name="calculate_total_price")

    def calculate_total_price(self, cart: Cart):
        return sum(item.quantity * item.product.unit_price for item in cart.items.all())

    class Meta:
        model = Cart
        fields = ("id", "total_price", "items")


########################### REVIEWS ###################################################
class ReviewSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        product = Product.objects.get(pk=self.context["product_id"])
        return Review.objects.create(product=product, **validated_data)

    class Meta:
        model = Review
        fields = ("id", "author", "review", "created_at")
