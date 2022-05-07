import uuid
from django.db import models


class Promotion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self) -> str:
        return self.title


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        "Product", on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )  # Does not create reverse relationship

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["title"]


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)  # Search engine optimization
    description = models.TextField(blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion, blank=True)

    def __str__(self) -> str:
        return self.title


class Customer(models.Model):
    MEMBERSHIP_GOLD = "G"
    MEMBERSHIP_SILVER = "S"
    MEMBERSHIP_BRONZE = "B"

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_GOLD, "Gold"),
        (MEMBERSHIP_SILVER, "Silver"),
        (MEMBERSHIP_BRONZE, "Bronze"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE
    )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Meta:
        indexes = [
            models.Index(fields=["first_name", "last_name"]),
        ]


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, primary_key=True
    )
    zipcode = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.street}, {self.city}, {self.zipcode}"


class Order(models.Model):
    PAYMENT_STATUS_PENDING = "P"
    PAYMENT_STATUS_COMPLETE = "C"
    PAYMENT_STATUS_FAILED = "F"

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, "Pending"),
        (PAYMENT_STATUS_COMPLETE, "Complete"),
        (PAYMENT_STATUS_FAILED, "Failed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING
    )
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f"{self.payment_status} - {self.customer.first_name}"


class OrderItem(models.Model):  # OrderItem is a join table
    quantity = models.PositiveSmallIntegerField()
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.product} - {self.quantity}"


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):  # CartItem is a join table
    quantity = models.PositiveSmallIntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.product} - {self.quantity}"
