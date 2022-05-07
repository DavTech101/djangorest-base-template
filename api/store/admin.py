from django.contrib import admin
from .models import Collection, Customer, Product, Promotion

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Promotion)
admin.site.register(Collection)
