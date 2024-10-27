from django.contrib import admin
from .models import PizzaCategory, Pizza, Cart, CartItem

@admin.register(PizzaCategory)
class PizzaCategoryAdmin(admin.ModelAdmin):
    list_display = ('uid', 'category_name', 'created_at', 'updated_at')
    search_fields = ('category_name',)

@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('uid', 'pizza_name', 'price', 'category', 'created_at', 'updated_at')
    search_fields = ('pizza_name',)
    list_filter = ('category',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('uid', 'user', 'is_paid', 'created_at', 'updated_at')
    search_fields = ('user__username',)
    list_filter = ('is_paid',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('uid', 'cart', 'pizza', 'created_at', 'updated_at')
    search_fields = ('cart__user__username', 'pizza__pizza_name')
    list_filter = ('cart',)

