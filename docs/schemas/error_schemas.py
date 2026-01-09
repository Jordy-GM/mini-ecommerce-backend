"""
Schemas personalizados para errores y respuestas
"""
from rest_framework import serializers


class ErrorResponseSerializer(serializers.Serializer):
    """Schema para respuestas de error genéricas"""
    error = serializers.CharField(help_text="Mensaje de error")


class MessageResponseSerializer(serializers.Serializer):
    """Schema para respuestas con mensaje de éxito"""
    message = serializers.CharField(help_text="Mensaje de confirmación")


class CartItemResponseSerializer(serializers.Serializer):
    """Schema para respuesta al agregar item"""
    message = serializers.CharField()
    item = serializers.DictField()


class SaveCartResponseSerializer(serializers.Serializer):
    """Schema para respuesta al guardar carrito"""
    message = serializers.CharField()
    cart = serializers.DictField()


class UpdateQuantityRequestSerializer(serializers.Serializer):
    """Schema para actualizar cantidad de item"""
    quantity = serializers.IntegerField(
        min_value=1,
        help_text="Nueva cantidad del producto (debe ser mayor a 0)"
    )


class ValidationErrorSerializer(serializers.Serializer):
    """Schema para errores de validación"""
    field_name = serializers.ListField(
        child=serializers.CharField(),
        help_text="Lista de errores para cada campo"
    )