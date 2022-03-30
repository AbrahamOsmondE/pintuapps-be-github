from django.contrib import admin
from django.http import HttpResponse

from user.models import Buyer
import csv
from .models import Order, OrderCustom, OrderItems
def download_csv(modeladmin, request, queryset):
    import csv
    f = open('some.csv', 'w')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(modeladmin)
    writer = csv.writer(response)
    writer.writerow(["Name", "Address", "Contact", "Item Name", "Quantity"])
    for s in queryset:
        print(s.to_user_id)
        name = Buyer.objects.get(user=s.to_user_id).name
        address = Buyer.objects.get(user=s.to_user_id).address
        contact = Buyer.objects.get(user=s.to_user_id).contact_number
        item_name = s.shopitem_id.item_name
        writer.writerow([name, address, contact, item_name, s.quantity])
    return response

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'is_submitted', 'paid')

    def user_name(self, obj):
        name = Buyer.objects.get(user=obj.from_user_id).name
        return name


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("to_user_name", "to_user_address",
                    "to_user_contact", "shop_item_name")
    list_filter = ('shopitem_id__shop_id',)
    actions = [download_csv]

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
    list_display = ("order_item_id", "value")


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItems, OrderItemAdmin)
admin.site.register(OrderCustom, OrderCustomAdmin)
# Register your models here.
