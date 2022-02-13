# API

Roughly follows [REST API](https://restfulapi.net/).
Front End [Figma](https://www.figma.com/file/Dq6ol6u0DSKJ0xGMuNF08d/PINTU-App-Interface?node-id=286%3A1953)
HTTP Method used:

| HTTP Method | CRUD Equivalent |
| ----------- | --------------- |
| POST        | Create          |
| GET         | Read            |
| PUT         | Update          |
| DELETE      | Delete          |

## Message Format

```json
{
  "error_code": 0,
  "message": "success",
  "data": {
    "id": 1,
    "title": "Exam Wishes",
    "open_date": "4 March 2021",
    "closed_date": "10 March 2021",
    "delivery_date": "12 March 2021",
    "is_closed": true
  }
}
```

### Error Code

TBD

## Authentication and Authorisation

Use google auth libraries.

https://www.hacksoft.io/blog/google-oauth2-with-django-react-part-1

https://github.com/HackSoftware/Django-React-GoogleOauth2-Example/blob/97b194418bc42d6015c1aeae53965b709f93b629/server/auth/services.py

## API List

### Shop

#### `GET /shop_api/shops`

Request Parameter:

| Parameter Name | Type | Required | Description               |
| -------------- | ---- | -------- | ------------------------- |
| `google_id`    | int  | Depends  | User ID to filter against |

`google_id` is required for most request, unless an admin is accessing data from admin page.

Response Data

```json
{
  "shops": [
    {
      "id": 1,
      "shop_owner": "PINTU",
      "shop_name": "Exam Wishes",
      "description": "EWP GTD",
      "open_date": "4 March 2021",
      "display_picture": "https://pintusingapura.org/static/image/paket01-2021.jpg",
      "closed_date": "10 March 2021",
      "is_open": true
    },
    {
      "id": 2,
      "shop_owner": "PINTU",
      "shop_name": "Exam Wishes",
      "description": "EWP GTD",
      "open_date": "4 March 2021",
      "display_picture": "https://pintusingapura.org/static/image/paket01-2021.jpg",
      "closed_date": "10 March 2021",
      "is_open": true
    }
  ]
}
```

#### `GET /shop_api/shops/<shop_id>`

Request Parameter: `null`

Response Data

```json
{
  "id": 1,
  "shop_owner": "PINTU",
  "shop_name": "Exam Wishes",
  "description": "EWP GTD",
  "open_date": "4 March 2021",
  "display_picture": "https://pintusingapura.org/static/image/paket01-2021.jpg",
  "closed_date": "10 March 2021",
  "is_open": true,
  "custom_fields": [
    {
      "id": "1",
      "type": "dropdown",
      "placeholder": "",
      "options": "hall12,hall11, halltamarind"
    },
    {
      "id": "1",
      "type": "textbox",
      "placeholder": "Enter Address",
      "options": ""
    }
  ]
  "shop_items": [
    {
      "id": 1,
      "item_name": "Paket Manis",
      "description": "Manis",
      "price": 3.5,
      "original_quantity": 100,
      "quantity": 90,
      "display_picture": "https://pintusingapura.org/static/image/paket01-2021.jpg"
    },
    {
      "id": 2,
      "item_name": "Paket Manis",
      "description": "Manis",
      "price": 3.5,
      "original_quantity": 100,
      "quantity": 90,
      "display_picture": "https://pintusingapura.org/static/image/paket01-2021.jpg"
    }
  ]
}
```

#### `GET /shop_api/shops/<shop_id>/<shop_item_id>`

Request Parameter: `null`

Response Data

```json
{
    "id": 1,
    "item_name": "Paket Manis",
    "description": "Manis",
    "price": 3.5,
    "quantity": 100,
    "display_picture": "https://pintusingapura.org/static/image/paket01-2021.jpg"
  "custom_fields": [
    {
      "id": "1",
      "type": "dropdown",
      "placeholder": "",
      "options": "hall12,hall11, halltamarind"
    },
    {
      "id": "1",
      "type": "textbox",
      "placeholder": "Enter Address",
      "options": ""
    }
  ]
}
```

#### `PUT /shop_api/shops/<shop_id>`

Request Parameter :

```json
{
    "id": 1,
    "shop_owner": "PINTU"
    "shop_name": "Exam Wishes",
    "description":"EWP GTD"
    "open_date": "4 March 2021",
    "display_picture": "https://pintusingapura.org/static/image/paket01-2021.jpg",
    "closed_date": "10 March 2021",
    "is_open": true,
    "custom_fields":[{
        "id":"1",
        "type":"dropdown",
        "placeholder":"",
        "options":"hall12,hall11, halltamarind",
    },
    {
        "id":"1",
        "type":"textbox",
        "placeholder":"Enter Address",
        "options":""
    }],
    "shop_items": [{
        "id": 1,
        "item_name": "Paket Manis",
        "description": "Manis",
        "price": 3.5,
        "quantity": 100,
        "display_picture": "https://pintusingapura.org/static/image/paket01-2021.jpg",
    },{
        "id": 2,
        "item_name": "Paket Manis",
        "description": "Manis",
        "price": 3.5,
        "quantity": 100,
        "display_picture": "https://pintusingapura.org/static/image/paket01-2021.jpg",
    }]
}

```

Response Data

```json
{
    "id": 1,
    "shop_owner": "PINTU"
    "shop_name": "Exam Wishes",
    "description":"EWP GTD"
    "open_date": "4 March 2021",
    "display_picture": "https://pintusingapura.org/static/image/paket01-2021.jpg",
    "closed_date": "10 March 2021",
    "is_open": true,
    "custom_fields":[{
        "id":"1",
        "type":"dropdown",
        "placeholder":"",
        "options":"hall12,hall11, halltamarind",
    },
    {
        "id":"1",
        "type":"textbox",
        "placeholder":"Enter Address",
        "options":""
    }],
    "shop_items": [{
        "id": 1,
        "item_name": "Paket Manis",
        "description": "Manis",
        "price": 3.5,
        "quantity": 100,
        "display_picture": "https://pintusingapura.org/static/image/paket01-2021.jpg",
    },{
        "id": 2,
        "item_name": "Paket Manis",
        "description": "Manis",
        "price": 3.5,
        "quantity": 100,
        "display_picture": "https://pintusingapura.org/static/image/paket01-2021.jpg",
    }]
}

```

#### `POST /shop_api/shops/<shop_id>`
<shop_id> ga kepake, itu cuman biar link semuanya sama, instead front end pass google_id biar kt tau owner shop siapa
Request Parameter :
| Parameter Name | Type | Required | Description               |
| -------------- | ---- | -------- | ------------------------- |
| `google_id`    | int  | Depends  | User ID to filter against |

`google_id` is required for most request, unless an admin is accessing data from admin page.


```json
{
    "google_id": "9182739873",
    "id": 1,
    "shop_owner": "PINTU"
    "shop_name": "Exam Wishes",
    "description":"EWP GTD"
    "open_date": "4 March 2021",
    "display_picture": "https://pintusingapura.org/static/image/paket01-2021.jpg",
    "closed_date": "10 March 2021",
    "is_open": true,
    "custom_fields":[{
        "id":"1",
        "type":"dropdown",
        "placeholder":"",
        "options":"hall12,hall11, halltamarind",
    },
    {
        "id":"1",
        "type":"textbox",
        "placeholder":"Enter Address",
        "options":""
    }],
    "shop_items": [{
        "id": 1,
        "item_name": "Paket Manis",
        "description": "Manis",
        "price": 3.5,
        "quantity": 100,
        "display_picture": "https://pintusingapura.org/static/image/paket01-2021.jpg",
    },{
        "id": 2,
        "item_name": "Paket Manis",
        "description": "Manis",
        "price": 3.5,
        "quantity": 100,
        "display_picture": "https://pintusingapura.org/static/image/paket01-2021.jpg",
    }]
}

```

Response Data

```json
{
  "id": 1,
  "shop_owner": "PINTU",
  "shop_name": "Exam Wishes",
  "description": "EWP GTD",
  "open_date": "4 March 2021",
  "display_picture": "https://pintusingapura.org/static/image/paket01-2021.jpg",
  "closed_date": "10 March 2021",
  "is_open": true,
  "custom_fields": [
    {
      "id": "1",
      "type": "dropdown",
      "placeholder": "",
      "options": "hall12,hall11, halltamarind"
    },
    {
      "id": "1",
      "type": "textbox",
      "placeholder": "Enter Address",
      "options": ""
    }
  ],
  "shop_items": [
    {
      "id": 1,
      "item_name": "Paket Manis",
      "description": "Manis",
      "price": 3.5,
      "quantity": 100,
      "display_picture": "https://pintusingapura.org/static/image/paket01-2021.jpg"
    },
    {
      "id": 2,
      "item_name": "Paket Manis",
      "description": "Manis",
      "price": 3.5,
      "quantity": 100,
      "display_picture": "https://pintusingapura.org/static/image/paket01-2021.jpg"
    }
  ]
}
```

#### `DELETE /api/shops/<shop_id>`

Request Parameter: `null`

Response Data: `null`

### ShopItem

#### `GET /shop_api/shop_item` [UNUSED FOR NOW]

Request Parameter: `null`

Response Data

```json
{
  "shop_id": 1,
  "products": [
    {
      "id": 1,
      "item_name": "Paket Manis",
      "description": "Manis",
      "price": 3.5,
      "quantity": 100,
      "display_picture": "https://pintusingapura.org/static/image/paket01-2021.jpg"
    },
    {
      "id": 2,
      "item_name": "Paket Asin",
      "description": "Asin",
      "price": 2.5,
      "quantity": 100,
      "display_picture": "https://pintusingapura.org/static/image/paket01-2021.jpg"
    },
    {
      "id": 3,
      "item_name": "Paket Panas Spesial",
      "description": "Asin dan Manis",
      "price": 5.5,
      "quantity": 100,
      "display_picture": "https://pintusingapura.org/static/image/paket01-2021.jpg"
    }
  ]
}
```

#### `GET /shop_api/shop_item/<shop_item_id>` [UNUSED FOR NOW]

Request Parameter: `null`

Response Data

```json
{
  "id": 1,
  "shop_id": 1,
  "item_name": "Paket Manis",
  "description": "Manis",
  "price": 3.5,
  "quantity": 100,
  "display_picture": "https://pintusingapura.org/static/image/paket01-2021.jpg"
}
```

#### `PUT /shop_api/shop_item/<shop_item_id>` [UNUSED FOR NOW]

Request Parameter

```json
{
  "id": 1,
  "shop_id": 1,
  "item_name": "Paket Manis",
  "description": "Manis",
  "price": 3.5,
  "quantity": 100,
  "display_picture": "https://pintusingapura.org/static/image/paket01-2021.jpg"
}
```

Response Data

```json
{
  "id": 1,
  "shop_id": 1,
  "item_name": "Paket Manis",
  "description": "Manis",
  "price": 3.5,
  "quantity": 100,
  "display_picture": "https://pintusingapura.org/static/image/paket01-2021.jpg"
}
```

### Order

#### `GET /order_api/order/buyer`

Request Parameter

| Parameter Name | Type | Required | Description               |
| -------------- | ---- | -------- | ------------------------- |
| `google_id`    | int  | Depends  | User ID to filter against |

`google_id` is required for most request, unless an admin is accessing data from admin page.

Response Data

```json
{
  "shops": [
    {
      "shop_name": "EWP PINTU",
      "order_id": 1,
      "orders": [
        {
          "item_name": "Paket Micin",
          "quantity": 5,
          "total_price": 15
        },
        {
          "item_name": "Paket Manis",
          "quantity": 5,
          "total_price": 12.5
        },
        {
          "item_name": "Paket Panas Special",
          "quantity": 5,
          "total_price": 25
        }
      ]
    },
    {
      "shop_name": "EWP GTD",
      "order_id": 2,
      "orders": [
        {
          "item_name": "Paket Micin",
          "quantity": 5,
          "total_price": 15
        },
        {
          "item_name": "Paket Manis",
          "quantity": 5,
          "total_price": 12.5
        },
        {
          "item_name": "Paket Panas Special",
          "quantity": 5,
          "total_price": 25
        }
      ]
    }
  ]
}
```

#### `GET /order_api/order/seller/<shop_id>`

Request Parameter

| Parameter Name | Type | Required | Description               |
| -------------- | ---- | -------- | ------------------------- |
| `google_id`    | int  | Depends  | User ID to filter against |

`google_id` is required for most request, unless an admin is accessing data from admin page.

Response Data

```json
{
  "shop_items": [
    {
      "shop_item_id": 1,
      "item_name": "Paket Manis",
      "description": "Manis",
      "price": 3.5,
      "quantity": 100,
      "sold": 10,
      "display_picture": "https://pintusingapura.org/static/image/paket01-2021.jpg"
    },
    {
      "shop_item_id": 2,
      "item_name": "Paket Asin",
      "description": "Asin",
      "price": 3.5,
      "quantity": 100,
      "sold": 10,
      "display_picture": "https://pintusingapura.org/static/image/paket01-2021.jpg"
    }
  ]
}
```

#### `GET /order_api/order/buyer/<order_id>`

Request Parameter

| Parameter Name | Type | Required | Description               |
| -------------- | ---- | -------- | ------------------------- |
| `google_id`    | int  | Depends  | User ID to filter against |

`google_id` is required for most request, unless an admin is accessing data from admin page.

Response Data

```json
{
  "order_id": 2,
  "shop_id": 1,
  "shop_name": "EWP GTD",
  "orders": [
    {
      "item_name": "Paket Micin",
      "quantity": 5,
      "total_price": 15,
      "order_customs": [
        {
          "type": "dropdown",
          "option": "hall12"
        },
        {
          "type": "text",
          "option": "1 #1-1-111"
        },
        {
          "type": "user",
          "option": "Daren"
        }
      ]
    },
    {
      "item_name": "Paket Manis",
      "quantity": 5,
      "total_price": 12.5,
      "order_customs": [
        {
          "type": "dropdown",
          "option": "hall12"
        },
        {
          "type": "text",
          "option": "1 #1-1-111"
        },
        {
          "type": "user",
          "option": "Daren"
        }
      ]
    },
    {
      "item_name": "Paket Panas Special",
      "quantity": 5,
      "total_price": 25,
      "order_customs": [
        {
          "type": "dropdown",
          "option": "hall12"
        },
        {
          "type": "text",
          "option": "1 #1-1-111"
        },
        {
          "type": "user",
          "option": "Daren"
        }
      ]
    }
  ]
}
```

#### `GET /order_api/order/seller/<order_id>`

Request Parameter

| Parameter Name | Type | Required | Description               |
| -------------- | ---- | -------- | ------------------------- |
| `google_id`    | int  | Depends  | User ID to filter against |

`google_id` is required for most request, unless an admin is accessing data from admin page.

Response Data

```json
{
  "order_id": 2,
  "shop_id": 1,
  "orders": [
    {
      "buyer_name": "Darren",
      "order_items": [
        {
          "shop_item_name":"Bundling Seito"
          "quantity": 3
          "total_price": 30
        },
        {
          "shop_item_name":"Bundling Sensei"
          "quantity": 4
          "total_price": 40
        }
      ],
    },
    {
      "buyer_name": "BC",
      "order_items": [
        {
          "shop_item_name":"Bundling Seito"
          "quantity": 3
          "total_price": 30
        },
        {
          "shop_item_name":"Bundling Sensei"
          "quantity": 4
          "total_price": 40
        }
      ],
    },
    {
      "buyer_name": "wesel",
      "order_items": [
        {
          "shop_item_name":"Bundling Seito"
          "quantity": 3
          "total_price": 30
        },
        {
          "shop_item_name":"Bundling Sensei"
          "quantity": 4
          "total_price": 40
        }
      ],
    }
  ]
}
```

#### `POST /order_api/order`

Request Parameter

| Parameter Name | Type | Required | Description               |
| -------------- | ---- | -------- | ------------------------- |
| `google_id`    | int  | Depends  | User ID to filter against |

```json
{
  "google_id": "9182739873",
  "shop_id": 1,
  "orders": [
    {
      "shopitem_id": 1,
      "quantity": 5,
      "total_price": 15,
      "order_customs": [
        {
          "type": "dropdown",
          "option": "hall12"
        },
        {
          "type": "text",
          "option": "1 #1-1-111"
        },
        {
          "type": "user",
          "option": "Daren"
        }
      ]
    },
    {
      "shopitem_id": 2,
      "quantity": 5,
      "total_price": 12.5,
      "order_customs": [
        {
          "type": "dropdown",
          "option": "hall12"
        },
        {
          "type": "text",
          "option": "1 #1-1-111"
        },
        {
          "type": "user",
          "option": "Daren"
        }
      ]
    },
    {
      "shopitem_id": 3,
      "quantity": 5,
      "total_price": 25,
      "order_customs": [
        {
          "type": "dropdown",
          "option": "hall12"
        },
        {
          "type": "text",
          "option": "1 #1-1-111"
        },
        {
          "type": "user",
          "option": "Daren"
        }
      ]
    }
  ]
}
```

Response Data

```json
{
  "order_id": 2,
  "shop_id": 1,
  "shop_name": "EWP GTD",
  "orders": [
    {
      "shopitem_id": 1,
      "quantity": 5,
      "total_price": 15,
      "order_customs": [
        {
          "type": "dropdown",
          "option": "hall12"
        },
        {
          "type": "text",
          "option": "1 #1-1-111"
        },
        {
          "type": "user",
          "option": "Daren"
        }
      ]
    },
    {
      "shopitem_id": 2,
      "quantity": 5,
      "total_price": 12.5,
      "order_customs": [
        {
          "type": "dropdown",
          "option": "hall12"
        },
        {
          "type": "text",
          "option": "1 #1-1-111"
        },
        {
          "type": "user",
          "option": "Daren"
        }
      ]
    },
    {
      "shopitem_id": 3,
      "quantity": 5,
      "total_price": 25,
      "order_customs": [
        {
          "type": "dropdown",
          "option": "hall12"
        },
        {
          "type": "text",
          "option": "1 #1-1-111"
        },
        {
          "type": "user",
          "option": "Daren"
        }
      ]
    }
  ]
}
```

#### `PUT /order_api/order/<order_id>`

Request Parameter

| Parameter Name | Type | Required | Description               |
| -------------- | ---- | -------- | ------------------------- |
| `google_id`    | int  | Depends  | User ID to filter against |

`google_id` is required for most request, unless an admin is accessing data from admin page.

Response Data

```json
{
  "order_id": 2,
  "shop_id": 1,
  "shop_name": "EWP GTD",
  "orders": [
    {
      "shopitem_id": 1,
      "quantity": 5,
      "total_price": 15,
      "order_customs": [
        {
          "type": "dropdown",
          "option": "hall12"
        },
        {
          "type": "text",
          "option": "1 #1-1-111"
        },
        {
          "type": "user",
          "option": "Daren"
        }
      ]
    },
    {
      "shopitem_id": 2,
      "quantity": 5,
      "total_price": 12.5,
      "order_customs": [
        {
          "type": "dropdown",
          "option": "hall12"
        },
        {
          "type": "text",
          "option": "1 #1-1-111"
        },
        {
          "type": "user",
          "option": "Daren"
        }
      ]
    },
    {
      "shopitem_id": 3,
      "quantity": 5,
      "total_price": 25,
      "order_customs": [
        {
          "type": "dropdown",
          "option": "hall12"
        },
        {
          "type": "text",
          "option": "1 #1-1-111"
        },
        {
          "type": "user",
          "option": "Daren"
        }
      ]
    }
  ]
}
```

#### `DELETE /order_api/order/<order_id>`

Request Parameter: `null`

Response Data: `null`

### Cart

#### `GET /cart_api/cart_items`

Request Parameter

| Parameter Name | Type | Required | Description               |
| -------------- | ---- | -------- | ------------------------- |
| `google_id`    | int  | Depends  | User ID to filter against |

`google_id` is required for most request, unless an admin is accessing data from admin page.

Response Data

```json
{
  "shops": [
    {
      "shop_name": "EWP PINTU",
      "shop_id": 1,
      "user_id": 1,
      "cart_items": [
        {
          "shopitem_id": 1,
          "item_name": "Paket Micin",
          "quantity": 5,
          "total_price": 15
        },
        {
          "shopitem_id": 2,
          "item_name": "Paket Manis",
          "quantity": 5,
          "total_price": 12.5
        },
        {
          "shopitem_id": 3,
          "item_name": "Paket Panas Special",
          "quantity": 5,
          "total_price": 25
        }
      ]
    },
    {
      "shop_name": "EWP GTD",
      "shop_id": 2,
      "user_id": 2,
      "orders": [
        {
          "shopitem_id": 1,
          "item_name": "Paket Micin",
          "quantity": 5,
          "total_price": 15
        },
        {
          "shopitem_id": 2,
          "item_name": "Paket Manis",
          "quantity": 5,
          "total_price": 12.5
        },
        {
          "shopitem_id": 3,
          "item_name": "Paket Panas Special",
          "quantity": 5,
          "total_price": 25
        }
      ]
    }
  ]
}
```

#### `GET /cart_api/cart_items/<shop_id>`

Request Parameter

| Parameter Name | Type | Required | Description               |
| -------------- | ---- | -------- | ------------------------- |
| `google_id`    | int  | Depends  | User ID to filter against |

`google_id` is required for most request, unless an admin is accessing data from admin page.

Response Data

```json
        {
            shop_name:"EWP PINTU",
            shop_id: 1
            user_id: 1,
            cart_items:[
                {
                    cart_item_id: 1,
                    item_name: "Paket Micin",
                    description: "Micin banget",
                    quantity: 5,
                    total_price: 15,
                    cart_item_customs: [{
                        type:"dropdown",
                        option:"hall12",
                    },
                    {
                        type:"text",
                        option:"1 #1-1-111",
                    },
                    {
                        type:"user",
                        option:"Daren"
                    }]
                },
                {
                    cart_item_id: 2,
                    item_name: "Paket Manis",
                    description: "Manis banget",
                    quantity: 5,
                    total_price: 12.5,
                    cart_item_customs: [{
                        type:"dropdown",
                        option:"hall12",
                    },
                    {
                        type:"text",
                        option:"1 #1-1-111",
                    },
                    {
                        type:"user",
                        option:"Daren"
                    }]
                },
                {
                    cart_item_id: 3,
                    item_name: "Paket Panas Special",
                    description: "Micin banget",
                    quantity: 5,
                    total_price: 25,
                    cart_item_customs: [{
                        type:"dropdown",
                        option:"hall12",
                    },
                    {
                        type:"text",
                        option:"1 #1-1-111",
                    },
                    {
                        type:"user",
                        option:"Daren"
                    }]
                }
            ]
        }
```

#### `POST /cart_api/cart_items`

Request Parameter

| Parameter Name | Type | Required | Description               |
| -------------- | ---- | -------- | ------------------------- |
| `google_id`    | int  | Depends  | User ID to filter against |

`google_id` is required for most request, unless an admin is accessing data from admin page.

```json
{
  "cart_items": [
    {
      "shop_item_id": 1,
      "quantity": 5,
      "cart_item_customs": [
        {
          "type": "dropdown",
          "option": "hall12"
        },
        {
          "type": "text",
          "option": "1 #1-1-111"
        },
        {
          "type": "user",
          "option": "Daren"
        }
      ]
    },
    {
      "shop_item_id": 2,
      "quantity": 5,
      "cart_item_customs": [
        {
          "type": "dropdown",
          "option": "hall12"
        },
        {
          "type": "text",
          "option": "1 #1-1-111"
        },
        {
          "type": "user",
          "option": "Daren"
        }
      ]
    },
    {
      "shop_item_id": 3,
      "quantity": 5,
      "cart_item_customs": [
        {
          "type": "dropdown",
          "option": "hall12"
        },
        {
          "type": "text",
          "option": "1 #1-1-111"
        },
        {
          "type": "user",
          "option": "Daren"
        }
      ]
    }
  ]
}
```

Response Data

```json
{
  "cart_items": [
    {
      "shop_item_id": 1,
      "quantity": 5,
      "cart_item_customs": [
        {
          "type": "dropdown",
          "option": "hall12"
        },
        {
          "type": "text",
          "option": "1 #1-1-111"
        },
        {
          "type": "user",
          "option": "Daren"
        }
      ]
    },
    {
      "shop_item_id": 2,
      "quantity": 5,
      "cart_item_customs": [
        {
          "type": "dropdown",
          "option": "hall12"
        },
        {
          "type": "text",
          "option": "1 #1-1-111"
        },
        {
          "type": "user",
          "option": "Daren"
        }
      ]
    },
    {
      "shop_item_id": 3,
      "quantity": 5,
      "cart_item_customs": [
        {
          "type": "dropdown",
          "option": "hall12"
        },
        {
          "type": "text",
          "option": "1 #1-1-111"
        },
        {
          "type": "user",
          "option": "Daren"
        }
      ]
    }
  ]
}
```

#### `PUT /cart_api/cart_items`

Request Parameter

| Parameter Name | Type | Required | Description               |
| -------------- | ---- | -------- | ------------------------- |
| `google_id`    | int  | Depends  | User ID to filter against |

`google_id` is required for most request, unless an admin is accessing data from admin page.

```json
{
  "cart_items": [
    {
      "shop_item_id": 1,
      "quantity": 5,
      "cart_item_customs": [
        {
          "type": "dropdown",
          "option": "hall12"
        },
        {
          "type": "text",
          "option": "1 #1-1-111"
        },
        {
          "type": "user",
          "option": "Daren"
        }
      ]
    },
    {
      "shop_item_id": 2,
      "quantity": 5,
      "cart_item_customs": [
        {
          "type": "dropdown",
          "option": "hall12"
        },
        {
          "type": "text",
          "option": "1 #1-1-111"
        },
        {
          "type": "user",
          "option": "Daren"
        }
      ]
    },
    {
      "shop_item_id": 3,
      "quantity": 5,
      "cart_item_customs": [
        {
          "type": "dropdown",
          "option": "hall12"
        },
        {
          "type": "text",
          "option": "1 #1-1-111"
        },
        {
          "type": "user",
          "option": "Daren"
        }
      ]
    }
  ]
}
```

Response Data

```json
{
  "cart_items": [
    {
      "shop_item_id": 1,
      "quantity": 5,
      "cart_item_customs": [
        {
          "type": "dropdown",
          "option": "hall12"
        },
        {
          "type": "text",
          "option": "1 #1-1-111"
        },
        {
          "type": "user",
          "option": "Daren"
        }
      ]
    },
    {
      "shop_item_id": 2,
      "quantity": 5,
      "cart_item_customs": [
        {
          "type": "dropdown",
          "option": "hall12"
        },
        {
          "type": "text",
          "option": "1 #1-1-111"
        },
        {
          "type": "user",
          "option": "Daren"
        }
      ]
    },
    {
      "shop_item_id": 3,
      "quantity": 5,
      "cart_item_customs": [
        {
          "type": "dropdown",
          "option": "hall12"
        },
        {
          "type": "text",
          "option": "1 #1-1-111"
        },
        {
          "type": "user",
          "option": "Daren"
        }
      ]
    }
  ]
}
```

#### `DELETE /cart_api/cart_items/<cart_item_id>`

Request Parameter

null

#### `DELETE /cart_api/shop_items/<shop_id>`

Request Parameter

| Parameter Name | Type | Required | Description               |
| -------------- | ---- | -------- | ------------------------- |
| `google_id`    | int  | Depends  | User ID to filter against |

`google_id` is required for most request, unless an admin is accessing data from admin page.

### User

TBD details from Authentication.

#### `GET /user_api/user/buyer`

Request Parameter

| Parameter Name | Type | Required | Description               |
| -------------- | ---- | -------- | ------------------------- |
| `google_id`    | int  | Depends  | User ID to filter against |

`google_id` is required for most request, unless an admin is accessing data from admin page.

Response Data:

```json
{
  "id": 1,
  "user_type":"buyer",
  "name": "Alice",
  "google_id": "67148129981274192471",
  "personal_email": "alice@gmail.com",
  "ntu_email": "alice@e.ntu.edu.sg",
  "contact_number": "88888888",
  "gender": "Other",
  "birth_date": "1 January 2021",
  "course": "Computer Science",
  "graduation_year": "2000",
  "address": "my address",
  "origin_city": "jakarta",
  "company": "NTU"
}
```

#### `GET /user_api/users/`

(Gets a list of every buyers for FE)
Request Parameter

Response Data:

```json
{
  "users": [
    {
      "name": "Daren",
      "user_id": 1
    },
    {
      "name": "BC",
      "user_id": 0
    },
    {
      "name": "Wessel",
      "user_id": 2
    }
  ]
}
```

#### `POST /user_api/user`
headers:
```json
{
  Authorization: "dsuhHuhdnbUbd81u" //data.accessToken, kalo bingung tnya daren
}
```
Request Parameter:`null`

```json
{
  "google_id": "67148129981274192471",
  "email": "alice@gmail.com",
}
```
Response Data:

```json
{
  "id": 1,
  "user_type":"buyer"
  "google_id": "67148129981274192471",
  "email": "alice@gmail.com",
  "token": "jisdhUTdjhustsbcT28ts71b9&g1B"
}
```

#### `PUT /user_api/user/buyer`

Request Parameter

| Parameter Name | Type | Required | Description               |
| -------------- | ---- | -------- | ------------------------- |
| `google_id`    | int  | Depends  | User ID to filter against |

`google_id` is required for most request, unless an admin is accessing data from admin page.

```json
{
  "id": 1,
  "name": "Alice",
  "google_id": "67148129981274192471",
  "personal_email": "alice@gmail.com",
  "ntu_email": "alice@e.ntu.edu.sg",
  "contact_number": "88888888",
  "gender": "Other",
  "birth_date": "1 January 2021",
  "course": "Computer Science",
  "graduation_year": "2000",
  "address": "my address",
  "origin_city": "jakarta",
  "company": "NTU"
}
```

Response Data:

```json
{
  "id": 1,
  "name": "Alice",
  "google_id": "67148129981274192471",
  "personal_email": "alice@gmail.com",
  "ntu_email": "alice@e.ntu.edu.sg",
  "contact_number": "88888888",
  "gender": "Other",
  "birth_date": "1 January 2021",
  "course": "Computer Science",
  "graduation_year": "2000",
  "address": "my address",
  "origin_city": "jakarta",
  "company": "NTU"
}
```

#### `POST /user_api/user/buyer`

Request Parameter

```json
{
  "id": 1,
  "name": "Alice",
  "google_id": "67148129981274192471",
  "personal_email": "alice@gmail.com",
  "ntu_email": "alice@e.ntu.edu.sg",
  "contact_number": "88888888",
  "gender": "Other",
  "birth_date": "1 January 2021",
  "course": "Computer Science",
  "graduation_year": "2000",
  "address": "my address",
  "origin_city": "jakarta",
  "company": "NTU"
}
```

Response Data:

```json
{
  "id": 1,
  "user_type":"buyer",
  "name": "Alice",
  "google_id": "67148129981274192471",
  "personal_email": "alice@gmail.com",
  "ntu_email": "alice@e.ntu.edu.sg",
  "contact_number": "88888888",
  "gender": "Other",
  "birth_date": "1 January 2021",
  "course": "Computer Science",
  "graduation_year": "2000",
  "address": "my address",
  "origin_city": "jakarta",
  "company": "NTU"
}
```

#### `POST /user_api/user/seller`

(Tentatif)
Request Parameter

```json
{
  "id": 1,
  "user_type":"buyer",
  "name": "Alice",
  "google_id": "67148129981274192471",
  "personal_email": "alice@gmail.com",
  "contact_number": "88888888",
  "gender": "Other"
}
```

Response Data:

```json
{
  "id": 1,
  "user_type":"buyer",
  "name": "Alice",
  "google_id": "67148129981274192471",
  "personal_email": "alice@gmail.com",
  "contact_number": "88888888",
  "gender": "Other"
}
```

#### `DELETE /user_api/user`

Request Parameter:

| Parameter Name | Type | Required | Description               |
| -------------- | ---- | -------- | ------------------------- |
| `google_id`    | int  | Depends  | User ID to filter against |

`google_id` is required for most request, unless an admin is accessing data from admin page.

Response Data: `null`
