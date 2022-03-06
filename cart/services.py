from .models import CartItem, CartCustom
from user.models import User, Buyer
from shop.models import Shop, ShopItem, ShopCustom

def get_cart_items(user_id):
    user = User.objects.filter(id=user_id).first()
    if not user:
        raise ValueError("No users found upon deletion!")
    shops = CartItem.objects.filter(user_id=user.id).select_related('shop_item_id').order_by('shop_item_id__shop_id').values('shop_item_id__shop_id').distinct()
    shops_list = []
    for shop in shops:
        shop_items = CartItem.objects.select_related('shop_item_id').filter(shop_item_id__shop_id=shop['shop_item_id__shop_id'], user_id=user.id).values('shop_item_id__id').distinct()
        shop_items_list = []
        for shop_item in shop_items:
            shop_items_objects = CartItem.objects.filter(shop_item_id=shop_item.get('shop_item_id__id'), user_id=user.id)
            shop_items_customs_quantity = 0
            for shop_items_object in shop_items_objects:
                shop_items_customs_quantity += shop_items_object.quantity
            item_detail = ShopItem.objects.filter(id=shop_item.get('shop_item_id__id')).first()
            shop_items_object = {
                "shopitem_id": item_detail.id,
                "display_picture": item_detail.display_picture,
                "item_name": item_detail.item_name,
                "quantity": shop_items_customs_quantity,
                "total_price": item_detail.price*shop_items_customs_quantity
            }
            shop_items_list.append(shop_items_object)
        shop_detail = Shop.objects.filter(id=shop['shop_item_id__shop_id']).first()
        shop_list = {
            "shop_name": shop_detail.shop_name,
            "shop_id": shop_detail.id,
            "user_id": user.id,
            "cart_items": shop_items_list
        }
        shops_list.append(shop_list)
    data = {
        "shops": shops_list
    }
    return data

def get_shop_cart_items(user_id, shop_id):
    user = User.objects.filter(id=user_id).first()
    if not user:
        raise ValueError("No users found upon deletion!")
    shop = Shop.objects.filter(id=shop_id).first()
    if not shop:
        raise ValueError("No shops found upon deletion!")
    shop_items = CartItem.objects.select_related('shop_item_id').filter(shop_item_id__shop_id=shop_id, user_id=user.id).values('shop_item_id__id').distinct()
    shop_customs_list = []
    shop_items_list = []
    shop_customs = ShopCustom.objects.filter(shop_id__id=shop_id)
    for shop_custom in shop_customs:
        shop_customs_list.append({
            "custom_field_id": shop_custom.id,
            "type": shop_custom.type,
            "placeholder": shop_custom.placeholder,
            "options": shop_custom.options
        })
    for shop_item in shop_items:
        shop_items_objects = CartItem.objects.filter(shop_item_id=shop_item.get('shop_item_id__id'), user_id=user.id)
        shop_items_customs_list = []
        shop_items_customs_quantity = 0
        for shop_items_object in shop_items_objects:
            shop_items_customs_map = []
            shop_items_customs = CartCustom.objects.filter(cart_item_id=shop_items_object.id)
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
            shop_items_customs_list.append({
                "cart_item_id": shop_items_object.id,
                "cart_items_customs": shop_items_customs_map
            })
        item_detail = ShopItem.objects.filter(id=shop_item.get('shop_item_id__id')).first()
        shop_items_object = {
            "item_name": item_detail.item_name,
            "description": item_detail.description,
            "quantity": shop_items_customs_quantity,
            "total_price": item_detail.price*shop_items_customs_quantity,
            "cart_item": shop_items_customs_list
        }
        shop_items_list.append(shop_items_object)
    shop_detail = Shop.objects.filter(id=shop_id).first()
    shop_list = {
        "shop_name": shop_detail.shop_name,
        "shop_id": shop_detail.id,
        "user_id": user.id,
        "custom_fields": shop_customs_list,
        "cart_items": shop_items_list
    }
    return shop_list

def post_cart_items(user_id, shop_item_id, quantity):
    user = User.objects.filter(id=user_id).first()
    shop_item = ShopItem.objects.filter(id=shop_item_id).first()
    if not user:
        raise ValueError("No users found upon deletion!")
    cart_item = CartItem(user_id=user, shop_item_id=shop_item, quantity=quantity)
    cart_item.save()
    return cart_item

def post_cart_custom(cart_item_id, shop_custom_id, value):
    cart_item = CartItem.objects.filter(id=cart_item_id).first()
    if not cart_item:
        raise ValueError("No cart items found upon deletion!")
    shop_custom = ShopCustom.objects.filter(id=shop_custom_id).first()
    if not shop_custom:
        raise ValueError("No shop customs found upon deletion!")
    cart_custom = CartCustom(cart_item_id=cart_item, shop_custom_id=shop_custom, value=value)
    cart_custom.save()

def put_cart_items(user_id, shop_item_id, cart_item_id, quantity):
    user = User.objects.filter(id=user_id).first()
    if not user:
        raise ValueError("No users found upon deletion!")
    cart_item = CartItem.objects.filter(cart_item_id=cart_item_id).first()
    if cart_item:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item = CartItem(user_id=user.user_id, shop_item_id=shop_item_id, quantity=quantity)
        cart_item.save()
    return cart_item

def put_cart_custom(cart_item_id, type, option):
    cart_custom = CartCustom(cart_item_id=cart_item_id, type=type, option=option)
    cart_custom.save()

def delete_cart_custom(cart_item_id):
    CartCustom.objects.filter(cart_item_id=cart_item_id).delete()

def delete_cart_items(cart_item_id):
    cart_item = CartItem.objects.filter(id=cart_item_id).first()
    if not cart_item:
        raise ValueError("No cart items found upon deletion!")
    cart_item.delete()

def delete_shop_cart_items(shop_item_id, user_id):
    user = User.objects.filter(id=user_id).first()
    if not user:
        raise ValueError("No users found upon deletion!")
    CartItem.objects.filter(shop_item_id=shop_item_id, user_id=user.id).delete()