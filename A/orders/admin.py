from django.contrib import admin

from orders.models import OrderItem, Order, Coupon


class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'updated', 'paid')
    list_filter = ('paid',)
    inlines = (OrderItemInLine,)


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_amount', 'valid_to', 'active']
