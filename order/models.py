from django.db import models
from shop.models import ShopCustom
from shop.models import ShopItem
from user.models import User
# Create your models here.


class Order(models.Model):
    is_submitted = models.BooleanField()
    paid = models.BooleanField(default=False)
    from_user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, default="")
    xanpay_id = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self) -> str:
        return str(self.id)


class OrderItems(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    shopitem_id = models.ForeignKey(ShopItem, on_delete=models.CASCADE)
    to_user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.id)


class OrderCustom(models.Model):
    value = models.TextField()
    order_item_id = models.ForeignKey(OrderItems, on_delete=models.CASCADE)
    shop_custom_id = models.ForeignKey(ShopCustom, on_delete=models.CASCADE)
