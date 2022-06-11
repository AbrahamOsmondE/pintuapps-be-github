from django.urls import path
from . import views

urlpatterns = [
    path('cart_items/',views.CartItemsAPI.as_view()),
    path('cart_items/<int:cart_item_id>/',views.SingleCartItemsAPI.as_view()),
    path('shop_items/<int:shop_id>/',views.ShopItemsAPI.as_view()),
    path('shop_item/<int:shop_item_id>/',views.SingleShopItemsAPI.as_view())
]
