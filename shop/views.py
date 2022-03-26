from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import date


# Create your views here.


class ShopsList(APIView):  # GET shops_api/shops/
    def get(self, request, format=None):
        user = User.objects.get(id=request.GET.get("user_id", ""))
        if user.user_type == "buyer":
            shops = Shop.objects.filter(is_open=True)
        else:
            shops = Shop.objects.filter(shop_owner_id=user, is_open=True)
        serializer = ShopsSerializer(shops, many=True)

        # Remove all closed shops
        months_to_int = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
                         "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}
        today = date.today()
        data = serializer.data
        invalid_indices = []  # Closed shops indices
        for i, shop in enumerate(data):
            open_date = shop["open_date"].split()  # [DD, Month, YYYY]
            closed_date = shop["closed_date"].split()  # [DD, Month, YYYY]
            open_date[1] = months_to_int[open_date[1]]
            closed_date[1] = months_to_int[closed_date[1]]
            open_date = list(map(int, open_date))[::-1]  # [YYYY, MM, DD]
            closed_date = list(map(int, closed_date))[::-1]  # [YYYY, MM, DD]
            open_date = date(*open_date)
            closed_date = date(*closed_date)
            if not open_date <= today <= closed_date:
                invalid_indices.append(i)
        invalid_indices = invalid_indices[::-1]
        for i in invalid_indices:
            data.pop(i)

        return Response({"shops": data})


class ShopDetails(APIView):  # GET, PUT, POST, DELETE shops_api/shops/<shop_id>
    def get(self, request, shop_id, format=None):
        shop = Shop.objects.get(id=shop_id)
        serializer = ShopSerializer(shop, many=False)
        return Response(serializer.data)

    def put(self, request, shop_id, format=None):
        shop = Shop.objects.get(id=shop_id)
        serializer = ShopSerializer(shop, data=request.data, many=False, context={
                                    'request': request.data})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, shop_id, format=None):
        user = User.objects.get(id=request.headers.get("user-id", ""))
        data = request.data
        data["shop_owner_id"] = user
        serializer = ShopSerializer(
            data=data, context={'request': data})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    def delete(self, request, shop_id, format=None):
        shop = Shop.objects.get(id=shop_id)
        shop.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ShopItemDetails(APIView):  # GET shops_api/shops/<shop_id>/<shop_item_id>/
    def get(self, request, shop_id, shop_item_id, format=None):
        shop = Shop.objects.get(id=shop_id)
        item = ShopItem.objects.get(id=shop_item_id, shop_id=shop_id)
        serializer = ShopItemSerializer(item, many=False)

        return Response(serializer.data)
