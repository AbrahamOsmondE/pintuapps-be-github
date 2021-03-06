from io import StringIO
import io
from itertools import chain
import os
from django.http import HttpResponse
from django.shortcuts import render
from cart.models import CartCustom
from .decorator import view_or_basicauth
from shop.models import Shop
from user.models import User, Seller, Buyer
from .serializers import BuyerOrderSerializer, OrderCustomSerializer, OrderListSerializer, OrderSerializer, OrderItemsSerializer, OrderCustomSerializer, SellerDetailedShopOrderSerializer, SellerOrderSerializer, ShopItemListSerializer, ShopOrderSerializer, ShopSerializer
from rest_framework.response import Response
from .models import Order, OrderItems, OrderCustom
from rest_framework.views import APIView
from rest_framework import status
import requests, json
from django.utils.decorators import method_decorator
from collections import defaultdict
from .services import *
import csv
import xlsxwriter
# Create your views here.


class BuyerOrdersList(APIView):  # GET /order_api/order/buyer
    authentication_classes = ()  # delete
    permission_classes = ()  # delete

    def get(self, request, format=None):
        user_id = request.GET['user_id']
        order_items = get_shop_items(user_id)
        return Response(data=order_items)
        '''
        user = User.objects.get(id=request.GET["user_id"])
        order = Order.objects.filter(from_user_id=user)
        serializer = ShopOrderSerializer(order, many=True)
        return Response(serializer.data)
        '''


class ShopItemList(APIView):  # GET /order_api/order/seller/<shop_id>
    authentication_classes = ()  # delete
    permission_classes = ()  # delete

    def get(self, request, shop_id, format=None):
        user = User.objects.get(id=request.GET["user_id"])
        shop = Shop.objects.get(shop_owner_id=user, id=shop_id)
        serializer = ShopSerializer(shop)
        return Response(serializer.data)


class BuyerOrder(APIView):  # GET /order_api/order/buyer/<order_id>
    authentication_classes = ()  # delete
    permission_classes = ()  # delete

    def get(self, request, order_id, format=None):
        user_id = request.GET['user_id']
        order_items = get_shop_order_items(user_id, order_id)
        return Response(data=order_items)
        '''
        user = User.objects.get(id=request.GET["user_id"])
        order = Order.objects.get(id=order_id)
        # check whether can use OrderSerializer or not
        serializer = BuyerOrderSerializer(order)
        return Response(serializer.data)
        '''


# GET /order_api/order/seller/detailed/<shop_id>
class SellerDetailedShopOrder(APIView):
    authentication_classes = ()  # delete
    permission_classes = ()  # delete

    def get(self, request, shop_id, format=None):
        shop = Shop.objects.get(id=shop_id)
        # check whether can use OrderSerializer or not
        serializer = SellerDetailedShopOrderSerializer(
            shop, context={'shop_id': shop_id})
        return Response(serializer.data)


class OrderList(APIView):  # POST /order_api/order
    authentication_classes = ()  # delete
    permission_classes = ()  # delete

    def post(self, request, format=None):
        user = User.objects.get(id=request.headers.get("user-id", ""))
        data = {}
        data["user"] = user
        data['shop_id'] = request.data['shop_id']
        serializer = OrderListSerializer(
            data=request.data, context={'request': data})
        if serializer.is_valid():
            serializer.save()

            serialized_data = serializer.data
            order_id = serialized_data["id"]
            serialized_data["order_id"] = serialized_data.pop("id")
            serialized_data["shop_name"] = list(Order.objects.get(pk=order_id).orderitems_set.all())[0].shopitem_id.shop_id.shop_name
            serialized_data["shop_id"] = list(Order.objects.get(pk=order_id).orderitems_set.all())[0].shopitem_id.shop_id.id
            
            return Response(serialized_data)
        return Response(serializer.errors)


class DeleteOrder(APIView):  # DELETE /order_api/order/<order_id>
    def delete(self, request, order_id, format=None):
        order = Order.objects.get(id=order_id)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderPayment(APIView):  # GET /order_api/order/buyer
    authentication_classes = ()  # delete
    permission_classes = ()  # delete

    def get(self, request, format=None):
        XANPAY_URL = "https://api.sandbox.xanpay.com/checkout-link"
        order_id = request.GET.get('order_id', '')
        user_id = request.GET.get('user_id', '')
        amount = 0

        response = dict()
        order = Order.objects.get(pk=order_id)
        user = User.objects.get(pk=user_id)

        for order_item in order.orderitems_set.all():
            amount += order_item.quantity*order_item.shopitem_id.price

        order_id = str(order.id)

        if len(order_id) < 3:
            order_id = "0"*(3-len(order_id)) + order_id

        response["paid"] = order.paid
        response["amount"] = amount
        response["order_id"] = list(order.orderitems_set.all())[0].shopitem_id.shop_id.custom_order_id + order_id
        response["shop_name"] = list(order.orderitems_set.all())[0].shopitem_id.shop_id.shop_name

        return Response(data=response)
        # if order.paid:
        #     response["checkoutLink"] = None
        #     return Response(data=response)

        # api_key = os.getenv("XANPAY_KEY")
        # api_secret = os.getenv("XANPAY_SECRET")
        # data = {
        #     "apiKey":api_key,
        #     "currency":"SGD",
        #     "amount":str(amount),
        #     "orders":[{
        #         "id": order_id,
        #         "quantity":1,
        #         "name":"PINTU App Purchase",
        #         "amount": amount
        #     }],
        #     "paymentMethods":{
        #         "SG": [
        #             "paynow"
        #         ]
        #     },
        #     "customer":{
        #         "email": user.email,}}
        # response["checkoutLink"] = requests.post(XANPAY_URL,json=data,auth=(api_key,api_secret)).json()["checkoutLink"]

        # return Response(data=response)

    @method_decorator(view_or_basicauth())
    def post(self, request, format=None):
        data = request.data
        order_id = data["data"]["orders"][0]["id"]
        order = Order.objects.get(pk=order_id)
        if data["event"] == "charge_completed":
            order.paid = True
            order.xanpay_id = data["data"]["id"]
        order.save()
        return Response(data=data)

class OrderPaymentStatus(APIView):  # GET /order_api/order/buyer
    authentication_classes = ()  # delete
    permission_classes = ()  # delete

    def get(self, request, format=None):
        order_id = request.GET.get('order_id', '')
        order = Order.objects.get(pk=order_id)

        data = {"paid":order.paid}
        return Response(data=data)

    def put(self,request):
        data = request.data
        order_id = data["order_id"]
        user_id = data["user_id"]
        paid = True if "paid" not in data else data["paid"]
        
        order = Order.objects.get(pk=order_id)

        order_items = list(order.orderitems_set.all())

        if len(order_items) == 0:
            raise ValueError("Invalid Order")

        shop_owner_id = order_items[0].shopitem_id.shop_id.shop_owner_id.id

        if int(shop_owner_id) == int(user_id):
            order.paid = paid
            order.save()
        else:
            raise ValueError("Incorrect Seller ID")
        
        data = {"paid":order.paid}
        return Response(data=data)

class OrderPaymentExcel(APIView):
    authentication_classes = ()  # delete
    permission_classes = ()  # delete

    def get(self,request,shop_id,format=None):
        shop = Shop.objects.get(id=shop_id)
        shop_name = shop.shop_name
        summary_worksheet = get_summary_worksheet(shop_id)
        details_worksheet = get_details_worksheet(shop_id)

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output,{'in_memory': True})

        summary = workbook.add_worksheet("Summary")
        details = workbook.add_worksheet("Details")

        for row,data in enumerate(summary_worksheet):
            for col,cell in enumerate(data):
                summary.write(row, col, cell)

        for row,data in enumerate(details_worksheet):
            for col,cell in enumerate(data):
                details.write(row,col,cell)
    
        workbook.close()

        #for more info https://xlsxwriter.readthedocs.io/example_http_server.html
        output.seek(0)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment;filename="{} Orders.xlsx"'.format(shop_name)
        response.write(output.read())

        return response