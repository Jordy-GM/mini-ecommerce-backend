"""
Decoradores personalizados para la documentación de Swagger
Products & Cart API
"""
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers


# ==================== SERIALIZERS INLINE PARA REQUESTS ====================

class AddCartItemRequestSerializer(serializers.Serializer):
    """Serializer para agregar item al carrito"""
    product_id = serializers.IntegerField(
        help_text="ID del producto a agregar",
        min_value=1
    )
    quantity = serializers.IntegerField(
        help_text="Cantidad del producto",
        min_value=1,
        default=1
    )


class UpdateQuantityRequestSerializer(serializers.Serializer):
    """Serializer para actualizar cantidad"""
    quantity = serializers.IntegerField(
        help_text="Nueva cantidad del producto (debe ser mayor a 0)",
        min_value=1
    )


class SaveCartItemSerializer(serializers.Serializer):
    """Serializer para items individuales en SaveCart"""
    product_id = serializers.IntegerField(
        help_text="ID del producto",
        min_value=1
    )
    quantity = serializers.IntegerField(
        help_text="Cantidad del producto",
        min_value=1
    )


class SaveCartRequestSerializer(serializers.Serializer):
    """Serializer para guardar carrito completo"""
    items = serializers.ListField(
        child=serializers.DictField(),
        help_text="Lista de items del carrito",
        allow_empty=False
    )


# ==================== PRODUCTS DECORATORS ====================

product_list_decorator = extend_schema(
    tags=['Products'],
    summary='Listar productos',
    description='Obtiene una lista de todos los productos activos. Permite filtrado por búsqueda y ordenamiento.',
    parameters=[
        OpenApiParameter(
            name='search',
            description='Buscar productos por nombre',
            required=False,
            type=OpenApiTypes.STR,
            examples=[
                OpenApiExample(
                    'Búsqueda simple',
                    value='laptop',
                    description='Busca productos que contengan "laptop" en el nombre'
                ),
            ],
        ),
        OpenApiParameter(
            name='ordering',
            description='Campo por el cual ordenar los resultados',
            required=False,
            type=OpenApiTypes.STR,
            enum=['-created_at', 'created_at', 'name', '-name', 'price', '-price'],
            default='-created_at',
            examples=[
                OpenApiExample('Más recientes primero', value='-created_at'),
                OpenApiExample('Precio ascendente', value='price'),
                OpenApiExample('Precio descendente', value='-price'),
            ],
        ),
    ],
    responses={
        200: {
            'description': 'Lista de productos obtenida exitosamente',
            'examples': {
                'application/json': {
                    'value': [
                        {
                            "id": 1,
                            "name": "Laptop HP Pavilion",
                            "description": "Laptop potente para trabajo",
                            "price": "899.99",
                            "stock": 15,
                            "image_url": "https://example.com/laptop.jpg",
                            "is_active": True,
                            "created_at": "2024-01-15T10:30:00Z"
                        }
                    ]
                }
            }
        },
    },
)


product_detail_decorator = extend_schema(
    tags=['Products'],
    summary='Obtener detalles de un producto',
    description='Obtiene la información completa de un producto específico por su ID.',
    responses={
        200: {
            'description': 'Producto encontrado exitosamente',
            'examples': {
                'application/json': {
                    'value': {
                        "id": 1,
                        "name": "Laptop HP Pavilion",
                        "description": "Laptop potente para trabajo y entretenimiento",
                        "price": "899.99",
                        "stock": 15,
                        "image_url": "https://example.com/laptop.jpg",
                        "is_active": True,
                        "created_at": "2024-01-15T10:30:00Z"
                    }
                }
            }
        },
        404: {
            'description': 'Producto no encontrado',
            'examples': {
                'application/json': {
                    'value': {'detail': 'No encontrado.'}
                }
            }
        },
    },
)


product_active_decorator = extend_schema(
    tags=['Products'],
    summary='Listar productos disponibles',
    description='Obtiene todos los productos activos que tienen stock disponible (stock > 0).',
    responses={
        200: {
            'description': 'Productos disponibles obtenidos exitosamente',
            'examples': {
                'application/json': {
                    'value': [
                        {
                            "id": 1,
                            "name": "Laptop HP Pavilion",
                            "description": "Laptop potente",
                            "price": "899.99",
                            "stock": 15,
                            "image_url": "https://example.com/laptop.jpg",
                            "is_active": True,
                            "created_at": "2024-01-15T10:30:00Z"
                        }
                    ]
                }
            }
        },
    },
)


# ==================== CART DECORATORS ====================

create_Cart = extend_schema(
    tags=['Cart'],
    summary='Crear carrito vacío',
    description='Crea un nuevo carrito vacío para comenzar a agregar productos.',
    request=None,
    responses={
        201: {
            'description': 'Carrito creado exitosamente',
            'examples': {
                'application/json': {
                    'value': {
                        'message': 'Carrito creado correctamente',
                        'cart': {
                            'id': 1,
                            'session_id': None,
                            'items': [],
                            'total': '0.00',
                            'total_items': 0,
                            'is_saved': False,
                            'created_at': '2025-01-09T20:30:00Z'
                        }
                    }
                }
            }
        },
    },
)


save_cart_decorator = extend_schema(
    tags=['Cart'],
    summary='Guardar carrito completo',
    description='Crea un nuevo carrito guardado con los items especificados. Valida stock y disponibilidad de productos.',
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'items': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'product_id': {
                                'type': 'integer',
                                'description': 'ID del producto',
                                'example': 1
                            },
                            'quantity': {
                                'type': 'integer',
                                'description': 'Cantidad del producto',
                                'example': 2,
                                'minimum': 1
                            }
                        },
                        'required': ['product_id', 'quantity']
                    },
                    'description': 'Lista de items del carrito'
                }
            },
            'required': ['items'],
            'example': {
                'items': [
                    {'product_id': 1, 'quantity': 2},
                    {'product_id': 3, 'quantity': 1}
                ]
            }
        }
    },
    responses={
        201: {
            'description': 'Carrito guardado exitosamente',
            'examples': {
                'application/json': {
                    'value': {
                        'message': 'Carrito guardado correctamente',
                        'cart': {
                            'id': 1,
                            'session_id': None,
                            'items': [
                                {
                                    'id': 1,
                                    'product': {
                                        'id': 1,
                                        'name': 'Laptop HP',
                                        'price': '899.99'
                                    },
                                    'quantity': 2,
                                    'subtotal': '1799.98'
                                }
                            ],
                            'total': '1799.98',
                            'total_items': 2,
                            'is_saved': True,
                            'created_at': '2024-01-20T14:30:00Z'
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Error de validación o stock insuficiente',
            'examples': {
                'application/json': {
                    'value': {'error': 'Stock insuficiente para Laptop HP. Disponible: 5'}
                }
            }
        },
        404: {
            'description': 'Producto no encontrado',
            'examples': {
                'application/json': {
                    'value': {'error': 'Producto con ID 999 no encontrado'}
                }
            }
        },
    },
)


cart_list_decorator = extend_schema(
    tags=['Cart'],
    summary='Listar carritos guardados',
    description='Obtiene todos los carritos que han sido guardados, ordenados por fecha de creación descendente.',
    responses={
        200: {
            'description': 'Lista de carritos obtenida exitosamente',
            'examples': {
                'application/json': {
                    'value': [
                        {
                            'id': 1,
                            'session_id': None,
                            'items': [],
                            'total': '1799.98',
                            'total_items': 2,
                            'is_saved': True,
                            'created_at': '2024-01-20T14:30:00Z',
                            'updated_at': '2024-01-20T14:30:00Z'
                        }
                    ]
                }
            }
        },
    },
)


cart_detail_get_decorator = extend_schema(
    tags=['Cart'],
    summary='Obtener detalles de un carrito',
    description='Obtiene la información completa de un carrito específico incluyendo todos sus items.',
    responses={
        200: {
            'description': 'Carrito encontrado exitosamente',
            'examples': {
                'application/json': {
                    'value': {
                        'id': 1,
                        'session_id': None,
                        'items': [
                            {
                                'id': 1,
                                'product': {
                                    'id': 1,
                                    'name': 'Laptop HP',
                                    'price': '899.99',
                                    'stock': 15
                                },
                                'quantity': 2,
                                'subtotal': '1799.98',
                                'created_at': '2024-01-20T14:30:00Z'
                            }
                        ],
                        'total': '1799.98',
                        'total_items': 2,
                        'is_saved': True,
                        'created_at': '2024-01-20T14:30:00Z',
                        'updated_at': '2024-01-20T14:30:00Z'
                    }
                }
            }
        },
        404: {
            'description': 'Carrito no encontrado',
            'examples': {
                'application/json': {
                    'value': {'detail': 'No encontrado.'}
                }
            }
        },
    },
)


cart_detail_delete_decorator = extend_schema(
    tags=['Cart'],
    summary='Eliminar carrito',
    description='Elimina permanentemente un carrito y todos sus items asociados.',
    responses={
        204: {
            'description': 'Carrito eliminado exitosamente'
        },
        404: {
            'description': 'Carrito no encontrado',
            'examples': {
                'application/json': {
                    'value': {'detail': 'No encontrado.'}
                }
            }
        },
    },
)


add_cart_item_decorator = extend_schema(
    tags=['Cart'],
    summary='Agregar item al carrito',
    description='Agrega un producto al carrito existente. Si el producto ya existe en el carrito, incrementa la cantidad.',
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'product_id': {
                    'type': 'integer',
                    'description': 'ID del producto a agregar',
                    'example': 1,
                    'minimum': 1
                },
                'quantity': {
                    'type': 'integer',
                    'description': 'Cantidad del producto',
                    'example': 2,
                    'minimum': 1,
                    'default': 1
                }
            },
            'required': ['product_id', 'quantity'],
            'example': {
                'product_id': 1,
                'quantity': 2
            }
        }
    },
    responses={
        200: {
            'description': 'Cantidad actualizada (producto ya existía en el carrito)',
            'examples': {
                'application/json': {
                    'value': {
                        'message': 'Item agregado correctamente',
                        'item': {
                            'id': 1,
                            'product': {
                                'id': 1,
                                'name': 'Laptop HP',
                                'price': '899.99'
                            },
                            'quantity': 5,
                            'subtotal': '4499.95'
                        }
                    }
                }
            }
        },
        201: {
            'description': 'Item creado exitosamente',
            'examples': {
                'application/json': {
                    'value': {
                        'message': 'Item agregado correctamente',
                        'item': {
                            'id': 2,
                            'product': {
                                'id': 2,
                                'name': 'Mouse Logitech',
                                'price': '79.99'
                            },
                            'quantity': 2,
                            'subtotal': '159.98'
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Stock insuficiente o validación fallida',
            'examples': {
                'application/json': {
                    'value': {'error': 'Stock insuficiente. Disponible: 3'}
                }
            }
        },
        404: {
            'description': 'Producto o carrito no encontrado',
            'examples': {
                'application/json': {
                    'value': {'error': 'Producto no encontrado'}
                }
            }
        },
    },
)


remove_cart_item_decorator = extend_schema(
    tags=['Cart'],
    summary='Eliminar item del carrito',
    description='Elimina un producto específico del carrito.',
    responses={
        204: {
            'description': 'Item eliminado exitosamente'
        },
        404: {
            'description': 'Item o carrito no encontrado',
            'examples': {
                'application/json': {
                    'value': {'detail': 'No encontrado.'}
                }
            }
        },
    },
)


update_cart_item_quantity_decorator = extend_schema(
    tags=['Cart'],
    summary='Actualizar cantidad de item',
    description='Actualiza la cantidad de un producto en el carrito. Valida que haya stock disponible.',
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'quantity': {
                    'type': 'integer',
                    'description': 'Nueva cantidad del producto (debe ser mayor a 0)',
                    'example': 5,
                    'minimum': 1
                }
            },
            'required': ['quantity'],
            'example': {
                'quantity': 5
            }
        }
    },
    responses={
        200: {
            'description': 'Cantidad actualizada exitosamente',
            'examples': {
                'application/json': {
                    'value': {
                        'message': 'Cantidad actualizada correctamente',
                        'item': {
                            'id': 1,
                            'product': {
                                'id': 1,
                                'name': 'Laptop HP',
                                'price': '899.99'
                            },
                            'quantity': 5,
                            'subtotal': '4499.95'
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Cantidad inválida o stock insuficiente',
            'examples': {
                'application/json': {
                    'value': {'error': 'La cantidad debe ser mayor a 0'}
                }
            }
        },
        404: {
            'description': 'Carrito o item no encontrado',
            'examples': {
                'application/json': {
                    'value': {'detail': 'No encontrado.'}
                }
            }
        },
    },
)