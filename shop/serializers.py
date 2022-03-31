from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework import serializers
from order.models import OrderItems


# GET shops_api/shops/
class ShopsSerializer(ModelSerializer):
    class Meta:
        model = Shop
        fields = ["id", "shop_owner", "shop_name", "description",
                  "open_date", "display_picture", "closed_date", "is_open"]


# GET shops_api/shops/<shop_id>/
class ShopCustomSerializer(ModelSerializer):
    class Meta:
        model = ShopCustom
        fields = ["id", "type", "placeholder", "options"]


# GET shops_api/shops/<shop_id>/
class ShopItemsSerializer(ModelSerializer):
    quantity = serializers.SerializerMethodField()

    class Meta:
        model = ShopItem
        fields = ["id", "item_name", "description", "original_quantity", "quantity",
                  "price", "display_picture"]

    # quantity field is original_quantity - sum of this item's quantity in all orders
    def get_quantity(self, obj):
        total = obj.original_quantity
        orders = OrderItems.objects.filter(shopitem_id=obj.id)
        for order in orders.values():
            total -= order["quantity"]
        return total


# GET, PUT, POST, DELETE shops_api/shops/<shop_id>/
class ShopSerializer(ModelSerializer):
    custom_fields = ShopCustomSerializer(
        source="shopcustom_set", many=True, read_only=True)
    shop_items = ShopItemsSerializer(
        many=True, read_only=True, source="shopitem_set")

    # POST
    def create(self, validated_data):
        data = self.context["request"]
        customFields = data.pop("custom_fields")
        shopItems = data.pop("shop_items")
        validated_data["shop_owner_id"] = data.pop("shop_owner_id")
        shop = Shop.objects.create(**validated_data)

        # Create the ShopCustom objects
        for shopcustom in customFields:
            custom_fields = ShopCustom(
                shop_id=shop, type=shopcustom["type"], placeholder=shopcustom["placeholder"], options=shopcustom["options"])
            custom_fields.save()

        # Create the ShopItem objects
        for shopitems in shopItems:
            shop_items = ShopItem(shop_id=shop, item_name=shopitems["item_name"], description=shopitems["description"],
                                  price=shopitems["price"], original_quantity=shopitems["original_quantity"], display_picture=shopitems.get("display_picture", ""))
            shop_items.save()

        return shop

    # PUT
    def update(self, instance, validated_data):
        data = self.context["request"]
        newCustomFields = data.pop("custom_fields")
        newShopItems = data.pop("shop_items")
        customFields = list(ShopCustom.objects.filter(shop_id=instance))
        shopItems = list(ShopItem.objects.filter(shop_id=instance))
        existing_shop_customs = set()
        existing_shop_items = set()

        for shopcustom in customFields:
            existing_shop_customs.add(int(shopcustom.id))

        for shopcustom in newCustomFields:
            if shopcustom.id in existing_shop_customs:
                custom_fields = ShopCustom.objects.get(id=shopcustom["id"])
                custom_fields.type = shopcustom["type"]
                custom_fields.placeholder = shopcustom["placeholder"]
                custom_fields.options = shopcustom["options"]
                custom_fields.save()
                existing_shop_customs.remove(shopcustom.id)
            else:
                custom_fields = ShopCustom(shop_id=instance, type=shopcustom["type"], placeholder=shopcustom["placeholder"], options=shopcustom["options"])
                custom_fields.save()

        for shopitems in shopItems:
            existing_shop_items.add(int(shopitems.id))

        for shopitems in newShopItems:
            if shopitems.id in existing_shop_items:
                shop_item = ShopItem.objects.get(id=shopitems["id"])
                shop_item.item_name = shopitems["item_name"]
                shop_item.description=shopitems["description"]
                shop_item.price=shopitems["price"]
                shop_item.original_quantity=shopitems["original_quantity"]
                shop_item.display_picture=shopitems.get("display_picture", "")
                shop_item.save()
                existing_shop_items.remove(shopitems.id)
            else:
                shop_item = ShopItem(shop_id=instance, item_name=shopitems["item_name"], description=shopitems["description"],
                                  price=shopitems["price"], original_quantity=shopitems["original_quantity"], display_picture=shopitems.get("display_picture", ""))
                shop_item.save()

        for shop_custom_id in existing_shop_customs:
            shop_custom = ShopCustom.objects.get(id=shop_custom_id)
            shop_custom.delete()
        
        for shop_item_id in existing_shop_items:
            shop_item = ShopItem.objects.get(id=shop_item_id)
            shop_item.delete()
            
        # Update the instance which is the Shop with the data
        instance.shop_owner = data.get(
            "shop_owner", instance.shop_owner)
        instance.shop_name = data.get(
            "shop_name", instance.shop_name)
        instance.description = data.get(
            "description", instance.description)
        instance.open_date = data.get(
            "open_date", instance.open_date)
        instance.display_picture = data.get(
            "display_picture", instance.display_picture)
        instance.closed_date = data.get(
            "closed_date", instance.closed_date)
        instance.is_open = data.get("is_open", instance.is_open)
        instance.custom_order_id = data.get("custom_order_id", instance.custom_order_id)
        instance.save()

        return instance

    class Meta:
        model = Shop
        fields = ["id", "shop_owner", "shop_name", "description",
                  "open_date", "display_picture","custom_order_id","closed_date", "is_open", "custom_fields", "shop_items"]


# GET shops_api/shops/<shop_id>/<shop_item_id>/
class ShopItemSerializer(ModelSerializer):
    custom_fields = ShopCustomSerializer(
        source="shop_id.shopcustom_set.all", many=True, read_only=True)
    quantity = serializers.SerializerMethodField()

    class Meta:
        model = ShopItem
        fields = ["id", "item_name", "description",
                  "price", "quantity", "display_picture", "custom_fields"]

    # quantity field is original_quantity - sum of this item's quantity in all orders
    def get_quantity(self, obj):
        total = obj.original_quantity
        orders = OrderItems.objects.filter(shopitem_id=obj.id)
        for order in orders.values():
            total -= order["quantity"]
        return total
