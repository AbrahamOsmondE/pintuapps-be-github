from django.urls import path
from . import views
urlpatterns = [
    path("shops/", views.ShopsList.as_view(), name="shops"),
    path("shops/<str:shop_id>/", views.ShopDetails.as_view(), name="shop"),
    path("shops/<str:shop_id>/<str:shop_item_id>/", views.ShopItemDetails.as_view(), name="item"),
    path("shop_item/<str:shop_item_id>",views.ShopItemAPI.as_view(),name="ShopItemAPI")
]
