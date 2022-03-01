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

    def __str__(self) -> str:
        return self.shop_name


class ShopItem(models.Model):
    shop_id = models.ForeignKey(Shop, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=30)
    description = models.TextField()
    price = models.FloatField()
    original_quantity = models.IntegerField(db_column="quantity")
    display_picture = models.BinaryField()

    def __str__(self) -> str:
        return self.item_name


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

    def __str__(self) -> str:
        return self.shop_id.shop_name + " (type: " + self.type + ")"
