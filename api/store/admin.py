from django.contrib import admin
from django.urls import reverse
from django.http import HttpRequest
from django.utils.html import format_html
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
    list_display = ("first_name", "last_name", "membership", "orders_count")

    @admin.display(ordering="orders_count")
    def orders_count(self, customer):
        url = f"{reverse('admin:store_order_changelist')}?customer={customer.id}"
        return format_html(f"<a href={url}>{customer.orders_count}</a>")

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(orders_count=Count("order"))


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
        url = f"{reverse('admin:store_product_changelist')}?collection__id={collection.id}"
        return format_html(f"<a href='{url}'>{collection.products_count}</a>")

    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).annotate(products_count=Count("product"))
