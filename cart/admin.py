from django.contrib import admin
from .models import Cart, CartProduct

@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'total_price')
    search_fields = ('product__name', 'cart__user__username')
    list_filter = ('product', 'cart__user')
    raw_id_fields = ('product', 'cart')

    def total_price(self, obj):
        return obj.total_price()
    
    total_price.short_description = 'Общая цена'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'cart_items', 'total_price_field')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email', 'created_at')

    def cart_items(self, obj):
        return ", ".join([str(item) for item in obj.items.all()])
    
    def total_price_field(self, obj):
        return obj.total_price
    
    cart_items.short_description = 'Список товаров'
    total_price_field.short_description = 'Общая цена'
