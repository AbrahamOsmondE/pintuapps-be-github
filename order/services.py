from .models import Order, OrderItems, OrderCustom
from user.models import User, Buyer
from shop.models import Shop, ShopItem, ShopCustom

def get_shop_items(user_id):
    user = User.objects.filter(id=user_id).first()
    if not user:
        raise ValueError("No users found upon deletion!")
    shops = OrderItems.objects.filter(order_id__from_user_id=user.id).select_related('shopitem_id').order_by('shopitem_id__shop_id').values('shopitem_id__shop_id').distinct()
    shops_list = []
    for shop in shops:
        orders = OrderItems.objects.filter(shopitem_id__shop_id=shop['shopitem_id__shop_id'], order_id__from_user_id=user.id).values('order_id').distinct()
        for order in orders:
            shop_items = OrderItems.objects.select_related('shopitem_id').filter(shopitem_id__shop_id=shop['shopitem_id__shop_id'], order_id__from_user_id=user.id, order_id=order['order_id']).values('shopitem_id__id').distinct()
            shop_items_list = []
            for shop_item in shop_items:
                shop_items_objects = OrderItems.objects.filter(shopitem_id=shop_item.get('shopitem_id__id'), order_id__from_user_id=user.id, order_id=order['order_id'])
                shop_items_customs_quantity = 0
                for shop_items_object in shop_items_objects:
                    shop_items_customs_quantity += shop_items_object.quantity
                item_detail = ShopItem.objects.filter(id=shop_item.get('shopitem_id__id')).first()
                shop_items_object = {
                    "display_picture": item_detail.display_picture,
                    "item_name": item_detail.item_name,
                    "description": item_detail.description,
                    "quantity": shop_items_customs_quantity,
                    "total_price": item_detail.price*shop_items_customs_quantity
                }
                shop_items_list.append(shop_items_object)
            shop_detail = Shop.objects.filter(id=shop['shopitem_id__shop_id']).first()
            shop_list = {
                "shop_name": shop_detail.shop_name,
                "order_id": order['order_id'],
                "orders": shop_items_list
            }
            shops_list.append(shop_list)
    data = {
        "shops": shops_list
    }
    return data

def get_shop_order_items(user_id, order_id):
    user = User.objects.filter(id=user_id).first()
    if not user:
        raise ValueError("No users found upon deletion!")
    order = Order.objects.filter(id=order_id).first()
    orderitem = OrderItems.objects.filter(order_id=order.id).first()
    shopitem = ShopItem.objects.filter(id=orderitem.shopitem_id.id).first()
    shop = Shop.objects.filter(id=shopitem.shop_id.id).first()
    if not shop:
        raise ValueError("No shops found upon deletion!")
    shop_items = OrderItems.objects.filter(order_id=order.id).distinct()
    shop_customs_list = []
    shop_items_list = []
    shop_customs = ShopCustom.objects.filter(shop_id__id=shop.id)
    for shop_custom in shop_customs:
        shop_customs_list.append({
            "custom_field_id": shop_custom.id,
            "type": shop_custom.type,
            "placeholder": shop_custom.placeholder,
            "options": shop_custom.options
        })
    for shop_item in shop_items:
        shop_items_objects = OrderItems.objects.filter(shopitem_id=shop_item.shopitem_id.id, order_id__from_user_id=user.id)
        shop_items_customs_list = []
        shop_items_customs_quantity = 0
        for shop_items_object in shop_items_objects:
            shop_items_customs_map = []
            shop_items_customs = OrderCustom.objects.filter(order_item_id=shop_items_object.id)
            shop_items_customs_quantity += shop_items_object.quantity
            for shop_items_custom in shop_items_customs:
                shop_custom = ShopCustom.objects.filter(id=shop_items_custom.shop_custom_id.id).first()
                if shop_custom.type == "user":
                    try:
                        user_option = Buyer.objects.select_related('user').filter(user__id=int(shop_items_custom.value)).first()
                        if user_option:
                            option = user_option.name
                        else:
                            option = "unknown user"
                    except:
                        option = "unknown user"
                    shop_items_customs_map.append({
                        "shop_custom_id": shop_custom.id,
                        "value": option
                    })
                else:
                    shop_items_customs_map.append({
                        "shop_custom_id": shop_custom.id,
                        "value": shop_items_custom.value
                    })
            shop_items_customs_list.append(shop_items_customs_map)
        item_detail = ShopItem.objects.filter(id=shop_item.shopitem_id.id).first()
        shop_items_object = {
            "item_name": item_detail.item_name,
            "quantity": shop_items_customs_quantity,
            "total_price": item_detail.price*shop_items_customs_quantity,
            "order_customs": shop_items_customs_list
        }
        shop_items_list.append(shop_items_object)
    shop_detail = Shop.objects.filter(id=shop.id).first()
    shop_list = {
        "shop_name": shop.shop_name,
        "shop_id": shop.id,
        "user_id": user.id,
        "custom_fields": shop_customs_list,
        "orders": shop_items_list
    }
    return shop_list