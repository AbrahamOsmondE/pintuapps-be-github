from .models import Order, OrderItems, OrderCustom
from user.models import User, Buyer, Seller
from shop.models import Shop, ShopItem, ShopCustom
from collections import defaultdict
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
                "custom_order_id": str(order['order_id']) + str(shop_detail.custom_order_id),
                "paid": Order.objects.filter(id=order['order_id']).first().paid,
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
    shop_items = OrderItems.objects.filter(order_id=order.id).distinct("shopitem_id")
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
        shop_items_objects = OrderItems.objects.filter(shopitem_id=shop_item.shopitem_id.id, order_id__from_user_id=user.id,order_id=order)
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
        "paid": order.paid,
        "custom_order_id": str(order_id) + str(shop.custom_order_id),
        "shop_id": shop.id,
        "user_id": user.id,
        "custom_fields": shop_customs_list,
        "orders": shop_items_list
    }
    return shop_list

def get_summary_worksheet(shop_id):
    shop = Shop.objects.get(id=shop_id)

    orders = defaultdict(dict)
    for shopitem in list(shop.shopitem_set.all()):
        for orderitem in list(shopitem.orderitems_set.all()):
            order = orderitem.order_id
            user = order.from_user_id

            try:
                name = Buyer.objects.get(user=user).name
                phone = Buyer.objects.get(user=user).contact_number

            except:
                name = Seller.objects.get(user=user).name
                phone = Seller.objects.get(user=user).contact_number
            
            orders[order.id]["Order ID"] = order.id
            orders[order.id]["Buyer"] = name
            orders[order.id]["Phone"] = phone
            orders[order.id]["Total Payment"] = orders[order.id].get("Total Payment",0) + orderitem.quantity * shopitem.price
            orders[order.id]["Payment Status"] = "Paid" if order.paid else "Awaiting Payment"
            orders[order.id][shopitem.item_name] = orders[order.id].get(shopitem.item_name,0) + orderitem.quantity

    worksheet1_headers = [["No","Order ID","Buyer","Phone","Total Payment","Payment Status"]]
    shopitems = set()
    for shopitem in list(shop.shopitem_set.all()):
        shopitems.add(shopitem.item_name)
    
    for shopitem in shopitems:
        worksheet1_headers[0].append(shopitem)

    worksheet1_list = []
    no = 1
    for order in orders:
        temp = [no]
        for col in worksheet1_headers[0]:
            if col == "No":
                continue
            temp.append(orders[order].get(col,0))
        worksheet1_list.append(temp[::])
        no += 1

    worksheet1_headers = worksheet1_headers + worksheet1_list

    return worksheet1_headers

def get_details_worksheet(shop_id):
    shop = Shop.objects.get(id=shop_id)

    order_items = defaultdict(dict)
    for shopitem in list(shop.shopitem_set.all()):
        for orderitem in list(shopitem.orderitems_set.all()):
            order = orderitem.order_id
            user = order.from_user_id

            try:
                name = Buyer.objects.get(user=user).name
                phone = Buyer.objects.get(user=user).contact_number

            except:
                name = Seller.objects.get(user=user).name
                phone = Seller.objects.get(user=user).contact_number
            
            order_items[orderitem.id]["Order ID"] = order.id
            order_items[orderitem.id]["Buyer"] = name
            order_items[orderitem.id]["Phone"] = phone
            order_items[orderitem.id]["Item Name"] = shopitem.item_name

            for ordercustom in list(orderitem.ordercustom_set.all()):
                shopcustom = ordercustom.shop_custom_id
                if shopcustom.type.lower() == "user":
                    receiver = User.objects.get(id=ordercustom.value)
                    try:
                        buyer = Buyer.objects.get(user=receiver)
                    except:
                        order_items[orderitem.id]["Receiver's Full Name"] = "Receiver not found"
                        order_items[orderitem.id]["Receiver's Address"] = "Receiver not found"
                        order_items[orderitem.id]["Receiver's Phone No."] = "Receiver not found"

                    order_items[orderitem.id]["Receiver's Full Name"] = buyer.name
                    order_items[orderitem.id]["Receiver's Address"] = buyer.address
                    order_items[orderitem.id]["Receiver's Phone No."] = buyer.contact_number

                else:
                    order_items[orderitem.id][shopcustom.placeholder] = ordercustom.value
            

    worksheet2_headers = [["No","Order ID","Buyer","Phone","Item Name"]]
    shopitem_customs = set()
    user_customs = set()
    for shop_custom in list(shop.shopcustom_set.all()):
        if shop_custom.type.lower() == "user":
            user_customs.add("Receiver's Full Name")
            user_customs.add("Receiver's Address")
            user_customs.add("Receiver's Phone No.")
        else:
            shopitem_customs.add(shop_custom.placeholder)
    
    for shop_custom in shopitem_customs:
        worksheet2_headers[0].append(shop_custom)
    for user_custom in user_customs:
        worksheet2_headers[0].append(user_custom)

    worksheet2_list = []
    for order_item in order_items:
        temp = []
        for col in worksheet2_headers[0]:
            if col == "No":
                continue
            temp.append(order_items[order_item].get(col,"N/A"))
        worksheet2_list.append(temp[::])

    worksheet2_list.sort(key=lambda i: i[0])

    for i in range(len(worksheet2_list)):
        worksheet2_list[i] = [i+1] + worksheet2_list[i]

    worksheet2_headers = worksheet2_headers + worksheet2_list

    return worksheet2_headers