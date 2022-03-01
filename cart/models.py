from django.db import models
from shop.models import ShopItem
from user.models import User

# Create your models here.
class CartItem(models.Model):
    shop_item_id = models.ForeignKey(ShopItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class CartCustom(models.Model):
    TYPE = (
        ('user', 'user'),
        ('text', 'text'),
        ('dropdown', 'dropdown')
    )
    cart_item_id = models.ForeignKey(CartItem, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=TYPE)
    option = models.TextField()
