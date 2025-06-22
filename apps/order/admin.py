from django.contrib import admin

# Register your models here.

from .models import  Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('get_total_price',)
    fields = ('product', 'quantity', 'price', 'discount', 'get_total_price')
    can_delete = True

    def get_total_price(self, obj):
        try:
            return obj.get_total_price()
        except Exception:
            return "-"
    get_total_price.short_description = "Сумма позиции"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'date', 'total_sum')
    list_filter = ('status', 'date')
    search_fields = ('customer__full_name', 'customer__email')
    inlines = [OrderItemInline]
    readonly_fields = ('total_sum', 'date')
