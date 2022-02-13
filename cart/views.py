from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .services import *

# Create your views here.

class CartItemsAPI(APIView):
    authentication_classes = ()
    permission_classes = ()
    def get(self,request,*args,**kwargs):
        google_id = request.GET['google_id']
        cart_items = get_cart_items(google_id)
        return Response(data=cart_items)

    def post(self,request,*args,**kwargs):
        google_id = request.GET['google_id']
        data = request.data
        for item in data['cart_items']:
            cart_item = post_cart_items(google_id,item['shop_item_id'],item['quantity'])
            for custom in item['cart_item_customs']:
                post_cart_custom(cart_item.id,custom['type'],custom['option'])
        return Response(data=data)

    def put(self,request,*args,**kwargs):
        google_id = request.GET['google_id']
        data = request.data
        for item in data['cart_items']:
            cart_item = put_cart_items(google_id,item['shop_item_id'],item['quantity'])
            delete_cart_custom(cart_item.id)
            for custom in item['cart_item_customs']:
                post_cart_custom(cart_item.id,custom['type'],custom['option'])
        return Response(data=data)

class SingleCartItemsAPI(APIView):
    authentication_classes = ()
    permission_classes = ()
    def delete(self,request,*args,**kwargs):
        cart_item_id = kwargs['cart_item_id']
        delete_cart_items(cart_item_id)
        return Response(status=status.HTTP_200_OK)

class ShopItemsAPI(APIView):
    authentication_classes = ()
    permission_classes = ()
    def get(self,request,*args,**kwargs):
        google_id = request.GET['google_id']
        shop_id = kwargs['shop_id']
        cart_items = get_shop_cart_items(google_id, shop_id)
        return Response(data=cart_items)

    def delete(self,request,*args,**kwargs):
        google_id = request.GET['google_id']
        shop_id = kwargs['shop_id']
        delete_shop_cart_items(shop_id, google_id)
        return Response(status=status.HTTP_200_OK)