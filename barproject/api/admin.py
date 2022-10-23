from django.contrib import admin

from .models import *

# Register your models here.
class BeerAdmin(admin.ModelAdmin):
    list_display = ("ref", "pk", "name", "description")

class BarAdmin(admin.ModelAdmin):
    list_display = ("name", "pk")

class StockAdmin(admin.ModelAdmin):
    list_display = ("reference", "bar", "stock", "pk")

class OrdersAdmin(admin.ModelAdmin):
    list_display = ("bar", "pk")

class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ("order", "reference", "count", "pk")

admin.site.register(Beer, BeerAdmin)
admin.site.register(Bar, BarAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(OrderItems, OrderItemsAdmin)