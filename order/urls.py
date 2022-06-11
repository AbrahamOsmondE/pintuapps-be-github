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
    path("order/", views.OrderList.as_view(), name="OrderList"),
    path("order/payment/",views.OrderPayment.as_view(),name="OrderPayment"),
    path("order/status/",views.OrderPaymentStatus.as_view(),name="OrderPaymentStatus"),
    path("order/excel/<str:shop_id>/",views.OrderPaymentExcel.as_view(),name="OrderPaymentExcel")
]
