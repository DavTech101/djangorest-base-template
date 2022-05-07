from django.contrib import admin
from .models import Collection, Customer, Product, Promotion


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_per_page = 100
    list_editable = ("inventory", "unit_price")
    list_display = ("title", "inventory", "unit_price")


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_per_page = 100
    list_editable = ("membership",)
    list_display = ("first_name", "last_name", "membership")


admin.site.register(Promotion)
admin.site.register(Collection)
