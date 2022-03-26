from django.urls import path
from . import views
urlpatterns = [
    path("order/buyer/", views.BuyerOrdersList.as_view(), name="buyerOrdersList"),
    path("order/seller/<str:shop_id>/",
         views.ShopItemList.as_view(), name="sellerOrderslist"),
    path("order/buyer/<str:order_id>/",
         views.BuyerOrder.as_view(), name="BuyerOrder"),
    path("order/seller/detailed/<str:shop_id>/",
         views.SellerDetailedShopOrder.as_view(), name="SellerDetailedShopOrder"),
    path("order/", views.OrderList.as_view(), name="OrderList")
]
