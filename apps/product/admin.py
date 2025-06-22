from django.contrib import admin

# Register your models here.
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','is_active','stock_quantity','price')
    list_filter = ('is_active',)