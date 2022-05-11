from django.urls import reverse
from tags.models import TaggedItem
from django.http import HttpRequest
from django.utils.html import format_html
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.db.models.aggregates import Count
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Collection, Customer, Product, Order, OrderItem


class InventoryFilter(admin.SimpleListFilter):
    title = "Inventory"
    parameter_name = "inventory"

    def lookups(self, request, model_admin):
        return [
            ("<10", "Low"),
            ("10-20", "Medium"),
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == "<10":
            return queryset.filter(inventory__lt=10)
        elif self.value() == "10-20":
            return queryset.filter(inventory__range=(10, 20))


class TagInline(GenericTabularInline):
    extra = 0
    model = TaggedItem
    autocomplete_fields = ("tag",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_per_page = 100
    inlines = [TagInline]
    search_fields = ("title",)
    actions = ("clear_inventory",)
    list_editable = ("unit_price",)
    autocomplete_fields = ("collection",)
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "inventory_status", "collection", "unit_price")
    list_filter = ("collection", "last_updated", "promotions", InventoryFilter)

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"

        return "OK"

    @admin.action(description="Clear inventory")
    def clear_inventory(self, request, queryset: QuerySet):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request, f"{updated_count} products updated", messages.SUCCESS
        )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_per_page = 100
    list_editable = ("membership",)
    ordering = ("first_name", "last_name")
    search_fields = (
        "first_name__istartswith",
        "last_name__istartswith",
        "email",
        "phone",
    )
    list_display = ("first_name", "last_name", "email", "membership", "orders_count")

    @admin.display(ordering="orders_count")
    def orders_count(self, customer):
        url = f"{reverse('admin:store_order_changelist')}?customer={customer.id}"
        return format_html(f"<a href={url}>{customer.orders_count} Orders</a>")

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(orders_count=Count("order"))


class OrderItemInline(admin.TabularInline):
    extra = 0
    model = OrderItem
    autocomplete_fields = ("product",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_per_page = 100
    inlines = (OrderItemInline,)
    autocomplete_fields = ("customer",)
    list_select_related = ("customer",)
    list_display = ("id", "customer", "placed_at")


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_per_page = 100
    search_fields = ("title",)
    list_display = ("title", "featured_product", "products_count")

    @admin.display(ordering="products_count")
    def products_count(self, collection):
        url = f"{reverse('admin:store_product_changelist')}?collection__id__exact={collection.id}"
        return format_html(f"<a href='{url}'>{collection.products_count}</a>")

    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).annotate(products_count=Count("product"))
