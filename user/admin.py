from django.contrib import admin
from django.http import HttpResponse
from .models import Buyer, Seller, User

# Register your models here.
def download_csv(modeladmin, request, queryset):
    import csv
    f = open('some.csv', 'w')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(modeladmin)
    writer = csv.writer(response)
    writer.writerow(["Name","Course","Graduation Year","Email", "Address", "Contact", "Gender", "Birthdate"])
    for s in queryset:
        name = s.name
        course = s.course
        grad = s.graduation_year
        email = s.user.email
        address = s.address
        contact = s.contact_number
        gender = s.gender
        birthdate = s.birth_date
        writer.writerow([name, course,grad,email,address, contact, gender,birthdate])
    return response
class UserAdmin(admin.ModelAdmin):
    list_display=('id','email','user_type')
    

class BuyerAdmin(admin.ModelAdmin):
    list_display=('id','name','address','contact_number')
    actions = [download_csv]

    def id(self,obj):
        return obj.user.id
    
class SellerAdmin(admin.ModelAdmin):
    list_display=('id', 'name', 'contact_number')

    def id(self,obj):
        return obj.user.id

admin.site.register(User, UserAdmin)
admin.site.register(Buyer, BuyerAdmin)
admin.site.register(Seller, SellerAdmin) 
