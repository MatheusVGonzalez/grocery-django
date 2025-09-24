from django.contrib import admin
from .models import *

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'get_full_name')
    list_filter = ('user_type',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email')
    
    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_full_name.short_description = 'Full Name'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'price', 'created_date', 'updated_date')
    list_filter = ('created_date', 'updated_date')
    search_fields = ('product_id', 'name')
    readonly_fields = ('created_date', 'updated_date')

class BasketItemInline(admin.TabularInline):
    model = BasketItem
    extra = 0
    readonly_fields = ('added_date',)

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'get_total_price', 'created_date', 'staff_reviewer')
    list_filter = ('status', 'created_date', 'review_date')
    search_fields = ('customer__username', 'customer__first_name', 'customer__last_name')
    readonly_fields = ('created_date', 'review_date', 'get_total_price')
    inlines = [BasketItemInline]
    
    def get_total_price(self, obj):
        return f"${obj.get_total_price()}"
    get_total_price.short_description = 'Total Price'

@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = ('basket', 'product', 'quantity', 'get_total_price', 'added_date')
    list_filter = ('added_date',)
    search_fields = ('basket__customer__username', 'product__name', 'product__product_id')
    readonly_fields = ('added_date',)
    
    def get_total_price(self, obj):
        return f"${obj.get_total_price()}"
    get_total_price.short_description = 'Total Price'

@admin.register(PurchaseHistory)
class PurchaseHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_amount', 'purchase_date', 'get_basket_id')
    list_filter = ('purchase_date',)
    search_fields = ('customer__username', 'customer__first_name', 'customer__last_name')
    readonly_fields = ('purchase_date',)
    
    def get_basket_id(self, obj):
        return f"Basket #{obj.basket.id}"
    get_basket_id.short_description = 'Basket'
