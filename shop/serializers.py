from rest_framework.serializers import ModelSerializer
from .models import *


class ShopsSerializer(ModelSerializer):
    class Meta:
        model = Shop
        fields = ["id", "shop_owner", "shop_name", "description",
                  "open_date", "display_picture", "closed_date", "is_open"]


class ShopCustomSerializer(ModelSerializer):
    class Meta:
        model = ShopCustom
        fields = ["id", "type", "placeholder", "options"]


class ShopItemSerializer(ModelSerializer):
    custom_fields = ShopCustomSerializer(
        source="shop_id.shopcustom_set.all", many=True, read_only=True)

    class Meta:
        model = ShopItem
        fields = ["id", "item_name", "description",
                  "price", "quantity", "display_picture", "custom_fields"]


class ShopItemsSerializer(ModelSerializer):
    class Meta:
        model = ShopItem
        fields = ["id", "item_name", "description",
                  "price", "quantity", "display_picture"]


class ShopSerializer(ModelSerializer):
    custom_fields = ShopCustomSerializer(
        source="shopcustom_set", many=True, read_only=True)
    shop_items = ShopItemsSerializer(
        many=True, read_only=True, source="shopitem_set")

    def create(self, validated_data):
        data = self.context["request"]
        customFields = data.pop("custom_fields")
        shopItems = data.pop("shop_items")
        validated_data["shop_owner_id"] = data.pop("shop_owner_id")
        shop = Shop.objects.create(**validated_data)
        for shopcustom in customFields:
            custom_fields = ShopCustom(
                shop_id=shop, type=shopcustom["type"], placeholder=shopcustom["placeholder"], options=shopcustom["options"])
            custom_fields.save()
        for shopitems in shopItems:
            shop_items = ShopItem(shop_id=shop, item_name=shopitems["item_name"], description=shopitems["description"],
                                  price=shopitems["price"], quantity=shopitems["quantity"], display_picture=shopitems.get("display_picture", b'asdf'))
            shop_items.save()
        return shop

    def update(self, instance, validated_data):
        data = self.context["request"]
        newCustomFields = data.pop("custom_fields")
        newShopItems = data.pop("shop_items")
        customFields = list(ShopCustom.objects.filter(shop_id=instance))
        shopItems = list(ShopItem.objects.filter(shop_id=instance))

        for shopcustom in customFields:
            shopcustom.delete()

        for shopcustom in newCustomFields:
            custom_fields = ShopCustom(
                shop_id=instance, type=shopcustom["type"], placeholder=shopcustom["placeholder"], options=shopcustom["options"])
            custom_fields.save()

        for shopitems in shopItems:
            shopitems.delete()

        for shopitems in newShopItems:
            shop_items = ShopItem(shop_id=instance, item_name=shopitems["item_name"], description=shopitems["description"],
                                  price=shopitems["price"], quantity=shopitems["quantity"], display_picture=shopitems.get("display_picture", b'asdf'))
            shop_items.save()

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
        instance.save()

        return instance

    class Meta:
        model = Shop
        fields = ["id", "shop_owner", "shop_name", "description",
                  "open_date", "display_picture", "closed_date", "is_open", "custom_fields", "shop_items"]
