from .models import CartItem, CartCustom
from user.models import User
from shop.models import Shop, ShopItem

def get_cart_items(google_id):
    user = User.objects.filter(google_id=google_id).first()
    if not user:
        raise ValueError("No users found upon deletion!")
    shops = CartItem.objects.filter(user_id=user.id).select_related('shop_item_id').order_by('shop_item_id__shop_id').values('shop_item_id__shop_id').distinct()
    shops_list = []
    for shop in shops:
        shop_id = shop.get('shop_item_id__shop_id')
        shop_items = CartItem.objects.select_related('shop_item_id').filter(shop_item_id__shop_id=shop_id, user_id=user.id)
        shop_items_list = []
        for shop_item in shop_items:
            shop_items_customs_map = []
            shop_items_customs = CartCustom.objects.filter(cart_item_id=shop_item.id)
            for shop_items_custom in shop_items_customs:
                shop_items_customs_map.append({
                    'type': shop_items_custom.type,
                    'option': shop_items_custom.option
                })
            item_detail = ShopItem.objects.filter(id=shop_item.shop_item_id.id).first()
            shop_items_object = {
                "cart_item_id": shop_item.id,
                "item_name": item_detail.item_name,
                "description": item_detail.description,
                "quantity": shop_item.quantity,
                "total_price": item_detail.price*shop_item.quantity,
                "cart_items_customs": shop_items_customs_map
            }
            shop_items_list.append(shop_items_object)
        shop_detail = Shop.objects.filter(id=shop_id).first()
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

def get_shop_cart_items(google_id, shop_id):
    user = User.objects.filter(google_id=google_id).first()
    if not user:
        raise ValueError("No users found upon deletion!")
    shop = Shop.objects.filter(id=shop_id).first()
    if not shop:
        raise ValueError("No shops found upon deletion!")
    shop_items = CartItem.objects.select_related('shop_item_id').filter(shop_item_id__shop_id=shop_id, user_id=user.id)
    shop_items_list = []
    for shop_item in shop_items:
        shop_items_customs_map = []
        shop_items_customs = CartCustom.objects.filter(cart_item_id=shop_item.id)
        for shop_items_custom in shop_items_customs:
            shop_items_customs_map.append({
                'type': shop_items_custom.type,
                'option': shop_items_custom.option
            })
        item_detail = ShopItem.objects.filter(id=shop_item.shop_item_id.id).first()
        shop_items_object = {
            "cart_item_id": shop_item.id,
            "item_name": item_detail.item_name,
            "description": item_detail.description,
            "quantity": shop_item.quantity,
            "total_price": item_detail.price*shop_item.quantity,
            "cart_items_customs": shop_items_customs_map
        }
        shop_items_list.append(shop_items_object)
    shop_detail = Shop.objects.filter(id=shop_id).first()
    shop_list = {
        "shop_name": shop_detail.shop_name,
        "shop_id": shop_detail.id,
        "user_id": user.id,
        "cart_items": shop_items_list
    }
    return shop_list

def post_cart_items(google_id, shop_item_id, quantity):
    user = User.objects.filter(google_id=google_id).first()
    if not user:
        raise ValueError("No users found upon deletion!")
    cart_item = CartItem.objects.filter(shop_item_id=shop_item_id, user_id=user.id).first()
    if cart_item:
        cart_item.quantity += quantity
        cart_item.save()
    else:
        cart_item = CartItem(user_id=user.user_id, shop_item_id=shop_item_id, quantity=quantity)
        cart_item.save()
    return cart_item

def post_cart_custom(cart_item_id, type, option):
    cart_item = CartItem.objects.filter(id=cart_item_id).first()
    if not cart_item:
        raise ValueError("No cart items found upon deletion!")
    cart_custom = CartCustom(cart_item_id=cart_item, type=type, option=option)
    cart_custom.save()

def put_cart_items(google_id, shop_item_id, quantity):
    user = User.objects.filter(google_id=google_id).first()
    if not user:
        raise ValueError("No users found upon deletion!")
    cart_item = CartItem.objects.filter(shop_item_id=shop_item_id, user_id=user.id).first()
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

def delete_shop_cart_items(shop_id, google_id):
    user = User.objects.filter(google_id=google_id).first()
    if not user:
        raise ValueError("No users found upon deletion!")
    CartItem.objects.filter(shop_item_id__shop_id=shop_id, user_id=user.id).delete()