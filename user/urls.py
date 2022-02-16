from django.urls import path
from . import views
from rest_framework_jwt.blacklist.views import BlacklistView
from rest_framework_jwt.views import refresh_jwt_token


urlpatterns = [
    path("auth/logout/", BlacklistView.as_view({"post": "create"})),
    path("api-token-refresh/", refresh_jwt_token),
    path('user/seller/',views.SellerAPI.as_view(), name="seller"),
    path('user/buyer/',views.BuyerAPI.as_view(), name="buyer"),
    path("user/",views.UserAPI.as_view(),name="user"),
    path("users/",views.UsersAPI.as_view(), name="users"),
    path("users_dummy/",views.UsersssAPI.as_view(), name="users"),
    path("otp/",views.OTPAPI.as_view(), name="otp")
]
