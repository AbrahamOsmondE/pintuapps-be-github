from django.contrib import admin
from .models import Buyer, Seller, User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display=('id','email','user_type')

class BuyerAdmin(admin.ModelAdmin):
    list_display=('id','name','address','contact_number')

    def id(self,obj):
        return obj.user.id
    
class SellerAdmin(admin.ModelAdmin):
    list_display=('id', 'name', 'contact_number')

    def id(self,obj):
        return obj.user.id

admin.site.register(User, UserAdmin)
admin.site.register(Buyer, BuyerAdmin)
admin.site.register(Seller, SellerAdmin) 
