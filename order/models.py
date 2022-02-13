from django.db import models

from shop.models import ShopItem
from user.models import User
# Create your models here.

class Order(models.Model):
    is_submitted = models.BooleanField()
    paid = models.BooleanField()

    def __str__(self) -> str:
        return self.id

class OrderItems(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    shopitem_id = models.ForeignKey(ShopItem, on_delete=models.CASCADE)
    from_user_id = models.ForeignKey(User, on_delete=models.CASCADE,related_name="from_user_id")
    to_user_id = models.ForeignKey(User, on_delete=models.CASCADE,related_name="to_user_id")
    
    def __str__(self) -> str:
        return self.id


class OrderCustom(models.Model):
    TYPE = (
        ('user', 'user'),
        ('text', 'text'),
        ('dropdown', 'dropdown')
    )
    type = models.CharField(max_length=100, choices=TYPE)
    option = models.TextField()
    order_item_id = models.ForeignKey(OrderItems, on_delete = models.CASCADE)
