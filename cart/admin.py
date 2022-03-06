from django.contrib import admin

from user.models import Buyer

from .models import CartItem, CartCustom


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('shop_item_name', 'user_name')

    def shop_item_name(self, obj):
        item_name = obj.shop_item_id.item_name
        return item_name

    def user_name(self, obj):
        name = Buyer.objects.get(user=obj.user_id).name
        return name


class CartCustomAdmin(admin.ModelAdmin):
    list_display = ("cart_item_id", "shop_item_name", "value")

    def shop_item_name(self, obj):
        item_name = obj.cart_item_id.shop_item_id.item_name
        return item_name


admin.site.register(CartItem, CartItemAdmin)
admin.site.register(CartCustom, CartCustomAdmin)
# Register your models here.
