from django.contrib import admin

from .models import CartCustom, CartItem

admin.site.register(CartItem)
admin.site.register(CartCustom)
# Register your models here.
