from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import date

# Function to know if a shop is open or not


def is_open_obj(shop):
    today = date.today()
    # Date is in the form YYYY-MM-DDTHH:mm:ss.SSSZ
    open_date = shop.open_date[:10].split("-")
    closed_date = shop.closed_date[:10].split("-")
    open_date = list(map(int, open_date))  # [YYYY, MM, DD]
    closed_date = list(map(int, closed_date))  # [YYYY, MM, DD]
    open_date = date(*open_date)
    closed_date = date(*closed_date)
    if open_date <= today <= closed_date:
        return True
    else:
        return False

def is_open_json(shop):
    today = date.today()
    # Date is in the form YYYY-MM-DDTHH:mm:ss.SSSZ
    open_date = shop["open_date"][:10].split("-")
    closed_date = shop["closed_date"][:10].split("-")
    open_date = list(map(int, open_date))  # [YYYY, MM, DD]
    closed_date = list(map(int, closed_date))  # [YYYY, MM, DD]
    open_date = date(*open_date)
    closed_date = date(*closed_date)
    if open_date <= today <= closed_date:
        return True
    else:
        return False


# GET shops_api/shops/
class ShopsList(APIView):
    authentication_classes = ()  # delete
    permission_classes = ()  # delete
    def get(self, request, format=None):
        user = User.objects.get(id=request.GET.get("user_id", ""))

        # If the user is a buyer, return all the open shops.
        if user.user_type == "buyer":
            shops = Shop.objects.filter(is_open=True)
            serializer = ShopsSerializer(shops, many=True)

            # Remove all closed shops.
            data = serializer.data
            invalid_indices = []  # Closed shops indices.
            for i, shop in enumerate(data):
                if not is_open_json(shop):
                    invalid_indices.append(i)
            invalid_indices = invalid_indices[::-1]
            for i in invalid_indices:
                data.pop(i)

        # If the user is a seller, return all shops owned by the user
        else:
            shops = Shop.objects.filter(shop_owner_id=user)
            serializer = ShopsSerializer(shops, many=True)
            data = serializer.data
        return Response({"shops": data})


# GET, PUT, POST, DELETE shops_api/shops/<shop_id>
class ShopDetails(APIView):
    authentication_classes = ()  # delete
    permission_classes = ()  # delete
    def get(self, request, shop_id, format=None):
        user = User.objects.get(id=request.GET.get("user_id", ""))
        shop = Shop.objects.get(id=shop_id)

        # If the user is a buyer, return the shop if it is open.
        if user.user_type == "buyer":
            if is_open_obj(shop):
                serializer = ShopSerializer(shop, many=False)
                return Response(serializer.data)
            return Response({})

        # If the user is a seller, check whether the user is the owner.
        else:
            # If the user is the shop owner, return the shop.
            if shop.shop_owner_id == user:
                serializer = ShopSerializer(shop, many=False)
                return Response(serializer.data)
            return Response({})

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


# GET shops_api/shops/<shop_id>/<shop_item_id>/
class ShopItemDetails(APIView):
    authentication_classes = ()  # delete
    permission_classes = ()  # delete
    def get(self, request, shop_id, shop_item_id, format=None):
        item = ShopItem.objects.get(id=shop_item_id, shop_id=shop_id)
        serializer = ShopItemSerializer(item, many=False)

        return Response(serializer.data)


class ShopItemAPI(APIView):
    authentication_classes = ()  # delete
    permission_classes = ()  # delete
    def put(self, request, shop_item_id, format=None):
        data = request.data
        shop_item = ShopItem.objects.get(id=shop_item_id)
        shop_item.original_quantity = int(data["quantity"])
        shop_item.save()
        serializer = ShopItemSerializer(shop_item, many=False)
        return Response(serializer.data)
