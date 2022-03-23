
from rest_framework import serializers
from cart.models import CartItem
from shop.models import ShopCustom

from user.models import Buyer, User
from .models import OrderItems, Order, OrderCustom
from shop.models import Shop, ShopItem
from itertools import chain
# BuyerOrdersList


class OrderItemsSerializer(serializers.ModelSerializer):
    item_name = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    def get_item_name(self, obj):
        item_name = obj.shopitem_id.item_name
        return item_name

    def get_total_price(self, obj):
        total_price = obj.quantity * obj.shopitem_id.price
        return total_price

    class Meta:
        model = OrderItems
        fields = ['item_name', 'quantity', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    orders = OrderItemsSerializer(
        source="orderitems_set", many=True, read_only=True)
    shop_name = serializers.SerializerMethodField()
    order_id = serializers.SerializerMethodField()

    def get_shop_name(self, obj):
        order_items = list(obj.orderitems_set.all())
        if len(order_items) == 0:
            return "Invalid Order"

        shop_name = order_items[
            0].shopitem_id.shop_id.shop_name
        return shop_name

    def get_order_id(self, obj):
        return obj.id

    class Meta:
        model = Order
        fields = ['shop_name', 'order_id', "orders"]


class ShopOrderSerializer(serializers.ModelSerializer):
    shops = OrderSerializer(source="*")

    class Meta:
        model = Order
        fields = ["shops"]

# ShopItem


class ShopItemListSerializer(serializers.ModelSerializer):
    shop_item_id = serializers.SerializerMethodField()
    sold = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()

    def get_sold(self, obj):

        orders = Order.objects.filter(orderitems__shopitem_id=obj, paid=True)
        print(list(orders))
        sold = 0
        for order in orders:
            sold += OrderItems.objects.get(
                order_id=order, shopitem_id=obj).quantity
        print(sold)
        return sold

    def get_shop_item_id(self, obj):
        return obj.id

    def get_quantity(self, obj):
        total = obj.original_quantity
        orders = OrderItems.objects.filter(shopitem_id=obj.id)
        for order in orders.values():
            total -= order["quantity"]
        return total

    class Meta:
        model = ShopItem
        fields = ["shop_item_id", "item_name", "description",
                  "price", "quantity", "sold", "display_picture"]


class ShopSerializer(serializers.ModelSerializer):
    shop_items = ShopItemListSerializer(
        source="shopitem_set", many=True, read_only=True)

    class Meta:
        model = Shop
        fields = ["shop_items"]


# BuyerOrder

class OrderCustomSerializer(serializers.ModelSerializer):
    shop_custom_id = serializers.SerializerMethodField()

    def get_shop_custom_id(self, obj):
        return obj.shop_custom_id.id

    class Meta:
        model = OrderCustom
        fields = ['shop_custom_id', 'value']


class BuyerOrderItemsSerializer(serializers.ModelSerializer):
    order_customs = OrderCustomSerializer(
        source="ordercustom_set", many=True, read_only=True)
    item_name = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    def get_item_name(self, obj):
        item_name = obj.shopitem_id.item_name
        return item_name

    def get_total_price(self, obj):
        total_price = obj.quantity * obj.shopitem_id.price
        return total_price

    class Meta:
        model = OrderItems
        fields = ['item_name', 'quantity', 'total_price', 'order_customs']


class BuyerOrderCustomFieldsSerializer(serializers.ModelSerializer):
    custom_field_id = serializers.SerializerMethodField()
    placeholder = serializers.SerializerMethodField()

    def get_custom_field_id(self, obj):
        print("object is ", obj)
        return obj.shop_custom_id.id

    def get_placeholder(self, obj):
        return obj.shop_custom_id.placeholder

    class Meta:
        model = OrderCustom
        fields = ["custom_field_id", "placeholder"]


class BuyerOrderSerializer(serializers.ModelSerializer):
    custom_fields = serializers.SerializerMethodField()
    orders = BuyerOrderItemsSerializer(
        source="orderitems_set", many=True, read_only=True)
    shop_name = serializers.SerializerMethodField()
    shop_id = serializers.SerializerMethodField()
    order_id = serializers.SerializerMethodField()

    def get_shop_name(self, obj):
        shop_name = list(obj.orderitems_set.all())[
            0].shopitem_id.shop_id.shop_name
        return shop_name

    def get_shop_id(self, obj):
        shop_id = list(obj.orderitems_set.all())[0].shopitem_id.shop_id.id
        return shop_id

    def get_order_id(self, obj):
        return obj.id

    def get_custom_fields(self, obj):
        order_items = list(obj.orderitems_set.all())
        order_customs = list(OrderCustom.objects.filter(
            order_item_id__in=order_items))
        serialized = []
        for custom in order_customs:
            serialized.append(BuyerOrderCustomFieldsSerializer(custom).data)
        return serialized

    class Meta:
        model = Order
        fields = ['order_id', 'shop_id',
                  'shop_name', "custom_fields", "orders"]


# SellerDetailedShopOrder

class SellerOrderItemsSerializer(serializers.ModelSerializer):
    shop_item_name = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    def get_shop_item_name(self, obj):
        shop_item_name = obj.shopitem_id.item_name
        return shop_item_name

    def get_total_price(self, obj):
        total_price = obj.quantity * obj.shopitem_id.price
        return total_price

    class Meta:
        model = OrderItems
        fields = ['shop_item_name', 'quantity', 'total_price']


class SellerOrderSerializer(serializers.Serializer):
    buyer_name = serializers.SerializerMethodField()
    order_items = SellerOrderItemsSerializer(
        source="orderitems_set", many=True)

    def get_buyer_name(self, obj):
        # order = OrderItems.objects.filter(list(orderitems_set.all())[
        #                                   0].shopitem_id.shop_id == obj.shop_id)
        user = obj.from_user_id
        buyer_name = Buyer.objects.get(user=user).name
        return buyer_name

    class Meta:
        model = Order
        fields = ['buyer_name', 'order_items']


class SellerDetailedShopOrderSerializer(serializers.ModelSerializer):
    shop_id = serializers.SerializerMethodField()
    # orders = SellerOrderSerializer(
    #     source="shopitem_set", many=True)
    orders = serializers.SerializerMethodField()

    def get_shop_id(self, obj):
        return obj.id

    def get_orders(self, obj):
        orderitemsset = []
        for shopitem in list(obj.shopitem_set.all()):
            orderitemsset = list(
                chain(orderitemsset, shopitem.orderitems_set.all()))
        print(orderitemsset)
        order_ids = []
        for i in orderitemsset:
            order_ids.append(i.order_id.id)
        u_order_ids = set(order_ids)
        referenced_orders = Order.objects.filter(
            id__in=u_order_ids)
        sellerorderitems = SellerOrderSerializer(
            referenced_orders, many=True)
        return sellerorderitems.data

    class Meta:
        model = Shop
        fields = ['shop_id', "orders"]


# post, kurang paham
class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ["order_id", "quantity", "shopitem_id", "to_user_id"]


class OrderListSerializer(serializers.ModelSerializer):
    orders = BuyerOrderItemsSerializer(
        source="orderitems_set", many=True, read_only=True)
    # shop_name = serializers.SerializerMethodField()
    # shop_id = serializers.SerializerMethodField()
    # order_id = serializers.SerializerMethodField()

    # def get_shop_name(self, obj):
    #     name = list(obj.orderitems_set.all())[0].shop_item_id.shop_id.name
    #     return name

    # def get_shop_id(self, obj):
    #     return obj.id

    # def get_order_id(self, obj):
    #     return obj.id
    # from user id kalau ga exist to user id = from user id

    def create(self, validated_data):
        data = self.context["request"]
        shop_id = data.pop("shop_id")
        user = data.pop("user")
        shop = Shop.objects.get(id=shop_id)
        cartitemset = []
        for shopitem in list(shop.shopitem_set.all()):
            cartitemset = list(
                chain(cartitemset, shopitem.cartitem_set.all().filter(user_id=user)))
        cartitemids = []
        for i in cartitemset:
            cartitemids.append(i.id)
        if len(cartitemids) == 0:
            return data
        order = Order.objects.create(
            is_submitted=True, paid=False, from_user_id=user)
        # print(order.orderitems_set.all())
        validated_data['order_id'] = order.id
        unique_cartitemids = set(cartitemids)
        # print(unique_cartitemids)
        for id in unique_cartitemids:
            cart = CartItem.objects.get(id=id)
            shopitem_id = cart.shop_item_id
            qty = cart.quantity
            # if cart
            # to_user_id =
            to_user_id = user

            for cart_custom in list(cart.cartcustom_set.all()):
                if cart_custom.shop_custom_id.type == "user":

                    user_id = int(cart_custom.value)
                    to_user_id = User.objects.get(id=user_id)
            orders = OrderItems.objects.create(
                order_id=order, quantity=qty, shopitem_id=shopitem_id, to_user_id=to_user_id)
            orders.save()
            for custom in list(cart.cartcustom_set.all()):
                order_customs = OrderCustom.objects.create(
                    order_item_id=orders, value=custom.value, shop_custom_id=custom.shop_custom_id)
                order_customs.save()
                custom.delete()
            cart.delete()
        return order

    class Meta:
        model = Order
        fields = ["orders"]
