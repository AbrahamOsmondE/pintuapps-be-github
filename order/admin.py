from django.contrib import admin

from user.models import Buyer

from .models import Order, OrderCustom, OrderItems


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'is_submitted', 'paid')

    def user_name(self, obj):
        name = Buyer.objects.get(user=obj.from_user_id).name
        return name


class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ("to_user_name", "to_user_address",
                    "to_user_contact", "shop_item_name")

    def to_user_name(self, obj):
        name = Buyer.objects.get(user=obj.to_user_id).name
        return name

    def to_user_address(self, obj):
        address = Buyer.objects.get(user=obj.to_user_id).address
        return address

    def to_user_contact(self, obj):
        contact = Buyer.objects.get(user=obj.to_user_id).contact_number
        return contact

    def shop_item_name(self, obj):
        item_name = obj.shopitem_id.item_name
        return item_name


class OrderCustomAdmin(admin.ModelAdmin):
    list_display = ("order_item_id", "type", "option")


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItems, OrderItemsAdmin)
admin.site.register(OrderCustom, OrderCustomAdmin)
# Register your models here.
