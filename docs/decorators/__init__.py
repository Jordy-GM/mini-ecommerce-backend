"""
Decoradores para documentación de Swagger
"""
from .swagger_decorators import (
    product_list_decorator,
    product_detail_decorator,
    product_active_decorator,
    save_cart_decorator,
    cart_list_decorator,
    cart_detail_get_decorator,
    cart_detail_delete_decorator,
    add_cart_item_decorator,
    remove_cart_item_decorator,
    update_cart_item_quantity_decorator,
)

__all__ = [
    'product_list_decorator',
    'product_detail_decorator',
    'product_active_decorator',
    'save_cart_decorator',
    'cart_list_decorator',
    'cart_detail_get_decorator',
    'cart_detail_delete_decorator',
    'add_cart_item_decorator',
    'remove_cart_item_decorator',
    'update_cart_item_quantity_decorator',
]