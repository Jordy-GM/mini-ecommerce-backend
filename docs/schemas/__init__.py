"""
Schemas personalizados para la documentación
"""
from .error_schemas import (
    ErrorResponseSerializer,
    MessageResponseSerializer,
    CartItemResponseSerializer,
    SaveCartResponseSerializer,
    UpdateQuantityRequestSerializer,
    ValidationErrorSerializer,
)

__all__ = [
    'ErrorResponseSerializer',
    'MessageResponseSerializer',
    'CartItemResponseSerializer',
    'SaveCartResponseSerializer',
    'UpdateQuantityRequestSerializer',
    'ValidationErrorSerializer',
]