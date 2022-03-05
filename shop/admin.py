from django.contrib import admin

from .models import Shop, ShopCustom, ShopItem

# admin.site.register(Shop)
# admin.site.register(ShopItem)
# admin.site.register(ShopCustom)
# Register your models here.


class ShopAdmin(admin.ModelAdmin):
    list_display = ("id", "shop_name", "shop_owner")


class ShopItemAdmin(admin.ModelAdmin):
    list_display = ("id", "shop_name", "original_quantity", "price")

    def shop_name(self, obj):
        return obj.shop_id.shop_name


class ShopCustomAdmin(admin.ModelAdmin):
    list_display = ("id", "shop_name", "type", "placeholder")

    def shop_name(self, obj):
        return obj.shop_id.shop_name


admin.site.register(Shop, ShopAdmin)
admin.site.register(ShopItem, ShopItemAdmin)
admin.site.register(ShopCustom, ShopCustomAdmin)
