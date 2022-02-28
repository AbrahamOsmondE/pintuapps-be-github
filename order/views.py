from itertools import chain
from django.shortcuts import render
from shop.models import Shop
from user.models import User
from .serializers import BuyerOrderSerializer, OrderCustomSerializer, OrderListSerializer, OrderSerializer, OrderItemsSerializer, OrderCustomSerializer, SellerDetailedShopOrderSerializer, SellerOrderSerializer, ShopItemListSerializer, ShopOrderSerializer, ShopSerializer
from rest_framework.response import Response
from .models import Order, OrderItems, OrderCustom
from rest_framework.views import APIView
from rest_framework import status
# Create your views here.


class BuyerOrdersList(APIView):  # GET /order_api/order/buyer
    authentication_classes = ()  # delete
    permission_classes = ()  # delete

    def get(self, request, format=None):
        user = User.objects.get(google_id=request.GET['google_id'])
        order = Order.objects.filter(from_user_id=user)
        serializer = ShopOrderSerializer(order, many=True)
        return Response(serializer.data)


class shopItemList(APIView):  # GET /order_api/order/seller/<shop_id>
    authentication_classes = ()  # delete
    permission_classes = ()  # delete

    def get(self, request, shop_id, format=None):
        print("tes")
        user = User.objects.get(google_id=request.GET['google_id'])
        shop = Shop.objects.get(shop_owner_id=user, id=shop_id)
        serializer = ShopSerializer(shop)
        return Response(serializer.data)


class BuyerOrder(APIView):  # GET /order_api/order/buyer/<order_id>
    authentication_classes = ()  # delete
    permission_classes = ()  # delete

    def get(self, request, order_id, format=None):
        user = User.objects.get(google_id=request.GET['google_id'])
        order = Order.objects.get(id=order_id)
        # check whether can use OrderSerializer or not
        serializer = BuyerOrderSerializer(order)
        return Response(serializer.data)


# GET /order_api/order/seller/detailed/<shop_id>
class SellerDetailedShopOrder(APIView):
    authentication_classes = ()  # delete
    permission_classes = ()  # delete

    def get(self, request, shop_id, format=None):
        shop = Shop.objects.get(id=shop_id)
        # check whether can use OrderSerializer or not
        serializer = SellerDetailedShopOrderSerializer(shop)
        return Response(serializer.data)


class OrderList(APIView):  # POST /order_api/order
    authentication_classes = ()  # delete
    permission_classes = ()  # delete

    def post(self, request, format=None):
        user = User.objects.get(google_id=request.GET['google_id'])
        data = request.data
        shop_id = data['shop_id']
        data['shop_id'] = shop_id
        data['user'] = user
        data['shop_name'] = Shop.objects.get(id=shop_id).shop_name
        serializer = OrderListSerializer(
            data=data, context={'request': data})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)


class DeleteOrder(APIView):  # DELETE /order_api/order/<order_id>
    def delete(self, request, order_id, format=None):
        order = Order.objects.get(id=order_id)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
