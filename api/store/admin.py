from django.contrib import admin
from django.http import HttpRequest
from django.db.models.aggregates import Count
from .models import Collection, Customer, Product, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_per_page = 100
    list_editable = ("unit_price",)
    list_display = ("title", "inventory_status", "collection", "unit_price")

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"

        return "OK"


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_per_page = 100
    list_editable = ("membership",)
    list_display = ("first_name", "last_name", "membership")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_per_page = 100
    list_select_related = ("customer",)
    list_display = ("id", "customer", "placed_at")


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_per_page = 100
    list_display = ("title", "featured_product", "products_count")

    @admin.display(ordering="products_count") 
    def products_count(self, collection):
        return collection.products_count

    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).annotate(products_count=Count("product"))
