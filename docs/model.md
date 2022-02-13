# Models
## Admin

## User
```json
{
    "id": 1,
    "user_type": "buyer",
    "google_id": "67148129981274192471",
    "email": "abraham.osmond@gmail.com"
}
```
## Buyer
Users will be logged in using Google OAuth
Address must follow this regex format: `^(\d+\w?\s#\d{1,2}\w?-\d+-\d+(s|S)?|non hall)$`.
Example:
- 1 #1-1-111
- 13 #13-1-1311
- 99 #99-99-9999
- non hall
```json
{
    "id": 1,
    "user_id": 1,
    "name": "Alice",
    "ntu_email": "alice@e.ntu.edu.sg",
    "contact_number": "88888888",
    "gender" : "Other",
    "birth_date": "1 January 2021",
    "course": "Computer Science",
    "graduation_year": "2000",
    "address": "my address",
    "origin_city": "jakarta",
    "company": "NTU",
}
```

## Seller 
```json
{
    "id": 1,
    "user_id": 1,
    "name": "Alice",
    "contact_number": "88888888",
    "gender" : "Other"
}
```

## Shop
### Display picture tanya Irvin :)
Do not calculate date on client!
```json
{
    "id": 1,
    "shop_owner": "PINTU"
    "shop_name": "Exam Wishes",
    "description":"EWP GTD"
    "open_date": "4 March 2021",
    "display_picture": "https://pintusingapura.org/static/image/paket01-2021.jpg",
    "closed_date": "10 March 2021",
    "is_open": true
}
```

## ShopItem
### Display picture tanya Irvin :)
```json
{
    "id": 1,
    "shop_id": 1,
    "item_name": "Paket Manis",
    "description": "Manis",
    "price": 3.5,
    "original_quantity":100,
    "quantity": 96,
    "display_picture": "https://pintusingapura.org/static/image/paket01-2021.jpg",
}
```

## Order
```json
{
    "id": 1,
    "from_user_id": 1,
    "to_user_id": 5,
    "is_submitted": false,
    "paid": true
}
```
## ShopCustom
```json
{
    id:1,
    shop_id:1,
    type:"checkbox",
    placeholder:"",
    options:"hall12,hall11,halltamarind",
}
```

## OrderCustom
```json
{
    id:1,
    order_item_id:1,
    type:"checkbox",
    option:"hall12",
}
```

## CartItem
```json
{ 
    "id": 1,
    "shop_item_id": 1,
    "quantity":100, 
    "user_id": 1
}
```

## CartCustom
```json
{
    id:1,
    cart_item_id:1,
    type:"checkbox",
    option:"hall12",
}
```
