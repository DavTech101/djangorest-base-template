from django.contrib import admin
from .models import Tag, TaggedItem


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_per_page = 100
    search_fields = ("label",)
