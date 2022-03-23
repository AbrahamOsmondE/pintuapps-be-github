from django.db import models
from shop.models import ShopItem, ShopCustom
from user.models import User

# Create your models here.


class CartItem(models.Model):
    shop_item_id = models.ForeignKey(
        ShopItem, on_delete=models.CASCADE, default="", blank=True, null=True)
    quantity = models.IntegerField(default=1)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class CartCustom(models.Model):
    cart_item_id = models.ForeignKey(CartItem, on_delete=models.CASCADE)
    shop_custom_id = models.ForeignKey(
        ShopCustom, on_delete=models.CASCADE, default="", blank=True, null=True)
    value = models.TextField()
