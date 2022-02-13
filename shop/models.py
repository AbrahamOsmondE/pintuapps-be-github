from django.db import models
from user.models import User
# Create your models here.


class Shop(models.Model):
    shop_owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
    shop_owner = models.CharField(max_length=100)
    shop_name = models.CharField(max_length=200)
    description = models.TextField()
    open_date = models.CharField(max_length=50)
    display_picture = models.BinaryField()
    is_open = models.BooleanField()
    closed_date = models.CharField(max_length=50)


class ShopItem(models.Model):
    shop_id = models.ForeignKey(Shop, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=30)
    description = models.TextField()
    price = models.FloatField()
    quantity = models.IntegerField()
    display_picture = models.BinaryField()


class ShopCustom(models.Model):
    TYPE = (
        ('user', 'user'),
        ('text', 'text'),
        ('dropdown', 'dropdown')
    )

    shop_id = models.ForeignKey(Shop, on_delete=models.CASCADE)
    type = models.CharField(max_length=30, choices=TYPE)
    placeholder = models.TextField()
    options = models.TextField(blank=True)
