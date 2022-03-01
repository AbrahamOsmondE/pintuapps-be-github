from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.


class ShopsList(APIView):
    authentication_classes = ()  # delete
    permission_classes = ()  # delete

    def get(self, request, format=None):
        user = User.objects.get(google_id=request.GET.get("google_id", ""))
        if user.user_type == "buyer":
            shops = Shop.objects.all()
        else:
            shops = Shop.objects.filter(shop_owner_id=user)
        serializer = ShopsSerializer(shops, many=True)

        return Response({"shops": serializer.data})


class ShopDetails(APIView):
    authentication_classes = ()  # delete
    permission_classes = ()  # delete

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
        user = User.objects.get(
            google_id=request.headers.get("google-id", ""))
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


class ShopItemDetails(APIView):
    authentication_classes = ()  # delete
    permission_classes = ()  # delete

    def get(self, request, shop_id, shop_item_id, format=None):
        shop = Shop.objects.get(id=shop_id)
        item = ShopItem.objects.get(id=shop_item_id, shop_id=shop_id)
        serializer = ShopItemSerializer(item, many=False)

        return Response(serializer.data)
