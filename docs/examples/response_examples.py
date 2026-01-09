"""
Ejemplos de respuestas para la documentación de Swagger
"""

# ==================== PRODUCTS EXAMPLES ====================

PRODUCT_LIST_EXAMPLE = [
    {
        "id": 1,
        "name": "Laptop HP Pavilion",
        "description": "Laptop potente para trabajo y entretenimiento",
        "price": "899.99",
        "stock": 15,
        "image_url": "https://example.com/images/laptop.jpg",
        "is_active": True,
        "created_at": "2024-01-15T10:30:00Z"
    },
    {
        "id": 2,
        "name": "Mouse Logitech MX Master",
        "description": "Mouse ergonómico inalámbrico",
        "price": "79.99",
        "stock": 50,
        "image_url": "https://example.com/images/mouse.jpg",
        "is_active": True,
        "created_at": "2024-01-14T15:20:00Z"
    },
    {
        "id": 3,
        "name": "Teclado Mecánico Corsair",
        "description": "Teclado mecánico RGB para gaming",
        "price": "129.99",
        "stock": 30,
        "image_url": "https://example.com/images/keyboard.jpg",
        "is_active": True,
        "created_at": "2024-01-13T09:15:00Z"
    }
]

PRODUCT_DETAIL_EXAMPLE = {
    "id": 1,
    "name": "Laptop HP Pavilion",
    "description": "Laptop potente para trabajo y entretenimiento con procesador Intel i7",
    "price": "899.99",
    "stock": 15,
    "image_url": "https://example.com/images/laptop.jpg",
    "is_active": True,
    "created_at": "2024-01-15T10:30:00Z"
}


# ==================== CART EXAMPLES ====================

CART_ITEM_EXAMPLE = {
    "id": 1,
    "product": {
        "id": 1,
        "name": "Laptop HP Pavilion",
        "description": "Laptop potente para trabajo y entretenimiento",
        "price": "899.99",
        "stock": 15,
        "image_url": "https://example.com/images/laptop.jpg",
        "is_active": True,
        "created_at": "2024-01-15T10:30:00Z"
    },
    "quantity": 2,
    "subtotal": "1799.98",
    "created_at": "2024-01-20T14:30:00Z"
}

CART_DETAIL_EXAMPLE = {
    "id": 1,
    "session_id": None,
    "items": [
        {
            "id": 1,
            "product": {
                "id": 1,
                "name": "Laptop HP Pavilion",
                "description": "Laptop potente",
                "price": "899.99",
                "stock": 15,
                "image_url": "https://example.com/images/laptop.jpg",
                "is_active": True,
                "created_at": "2024-01-15T10:30:00Z"
            },
            "quantity": 2,
            "subtotal": "1799.98",
            "created_at": "2024-01-20T14:30:00Z"
        },
        {
            "id": 2,
            "product": {
                "id": 2,
                "name": "Mouse Logitech",
                "description": "Mouse ergonómico",
                "price": "79.99",
                "stock": 50,
                "image_url": "https://example.com/images/mouse.jpg",
                "is_active": True,
                "created_at": "2024-01-14T15:20:00Z"
            },
            "quantity": 1,
            "subtotal": "79.99",
            "created_at": "2024-01-20T14:31:00Z"
        }
    ],
    "total": "1879.97",
    "total_items": 3,
    "is_saved": True,
    "created_at": "2024-01-20T14:30:00Z",
    "updated_at": "2024-01-20T14:31:00Z"
}

SAVE_CART_REQUEST_EXAMPLE = {
    "items": [
        {"product_id": 1, "quantity": 2},
        {"product_id": 2, "quantity": 1}
    ]
}

SAVE_CART_RESPONSE_EXAMPLE = {
    "message": "Carrito guardado correctamente",
    "cart": CART_DETAIL_EXAMPLE
}


# ==================== ERROR EXAMPLES ====================

ERROR_STOCK_INSUFFICIENT = {
    "error": "Stock insuficiente para Laptop HP Pavilion. Disponible: 5"
}

ERROR_PRODUCT_NOT_FOUND = {
    "error": "Producto con ID 999 no encontrado"
}

ERROR_INVALID_QUANTITY = {
    "error": "La cantidad debe ser mayor a 0"
}

ERROR_VALIDATION = {
    "items": [
        "Cada item debe tener 'product_id' y 'quantity'"
    ]
}

ERROR_CART_NOT_FOUND = {
    "detail": "No encontrado."
}

ERROR_ITEM_NOT_FOUND = {
    "detail": "Item no encontrado en el carrito."
}

ERROR_INVALID_DATA = {
    "success": False,
    "message": "Datos inválidos",
    "errors": {
        "product_id": ["Este campo es requerido."],
        "quantity": ["Este campo es requerido."]
    }
}