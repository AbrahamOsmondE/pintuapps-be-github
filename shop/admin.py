from django.contrib import admin

from .models import Shop, ShopCustom, ShopItem

admin.site.register(Shop)
admin.site.register(ShopItem)
admin.site.register(ShopCustom)
# Register your models here.
