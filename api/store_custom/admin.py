from django.contrib import admin
from store.models import Product
from tags.models import TaggedItem
from store.admin import ProductAdmin
from django.contrib.contenttypes.admin import GenericTabularInline


class TagInline(GenericTabularInline):
    extra = 0
    model = TaggedItem
    autocomplete_fields = ("tag",)


class CustomProductAdmin(ProductAdmin):
    inlines = (TagInline,)


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
