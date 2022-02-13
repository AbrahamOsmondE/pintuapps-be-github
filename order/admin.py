from django.contrib import admin

from .models import Order, OrderCustom, OrderItems


admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(OrderCustom)
# Register your models here.
