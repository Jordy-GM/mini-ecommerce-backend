from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.shortcuts import get_object_or_404

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer, SaveCartSerializer
from products.models import Product

# decoradores de documentación
from docs.decorators.swagger_decorators import (
    save_cart_decorator,
    cart_list_decorator,
    cart_detail_get_decorator,
    cart_detail_delete_decorator,
    add_cart_item_decorator,
    remove_cart_item_decorator,
    update_cart_item_quantity_decorator,
    create_Cart,
)


class SaveCartView(APIView):
    """
    POST: Guardar carrito completo desde el frontend
    """
    
    @save_cart_decorator
    def post(self, request):
        serializer = SaveCartSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                # Crear nuevo carrito
                cart = Cart.objects.create(is_saved=True)
                
                # Crear items del carrito
                items_data = serializer.validated_data['items']
                created_items = []
                
                for item_data in items_data:
                    try:
                        product = Product.objects.get(
                            id=item_data['product_id'],
                            is_active=True
                        )
                        
                        # Validar stock
                        if product.stock < item_data['quantity']:
                            return Response(
                                {
                                    'error': f'Stock insuficiente para {product.name}. Disponible: {product.stock}'
                                },
                                status=status.HTTP_400_BAD_REQUEST
                            )
                        
                        cart_item = CartItem.objects.create(
                            cart=cart,
                            product=product,
                            quantity=item_data['quantity']
                        )
                        created_items.append(cart_item)
                        
                    except Product.DoesNotExist:
                        return Response(
                            {'error': f'Producto con ID {item_data["product_id"]} no encontrado'},
                            status=status.HTTP_404_NOT_FOUND
                        )
                
                # Serializar respuesta
                cart_serializer = CartSerializer(cart)
                
                return Response(
                    {
                        'message': 'Carrito guardado correctamente',
                        'cart': cart_serializer.data
                    },
                    status=status.HTTP_201_CREATED
                )
                
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CartListView(APIView):
    """
    GET: Listar todos los carritos guardados
    """
    
    @cart_list_decorator
    def get(self, request):
        carts = Cart.objects.filter(is_saved=True).order_by('-created_at')
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartDetailView(APIView):
    """
    GET: Obtener detalles de un carrito específico
    DELETE: Eliminar un carrito
    """
    
    @cart_detail_get_decorator
    def get(self, request, pk):
        cart = get_object_or_404(Cart, pk=pk)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @cart_detail_delete_decorator
    def delete(self, request, pk):
        cart = get_object_or_404(Cart, pk=pk)
        cart.delete()
        return Response(
            {'message': 'Carrito eliminado correctamente'},
            status=status.HTTP_204_NO_CONTENT
        )


class AddCartItemView(APIView):
    """
    POST: Agregar item a un carrito existente
    """
    
    @add_cart_item_decorator
    def post(self, request, pk):
        cart = get_object_or_404(Cart, pk=pk)
        serializer = CartItemSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product = Product.objects.get(id=serializer.validated_data['product_id'])
            
            # Verificar stock
            if product.stock < serializer.validated_data['quantity']:
                return Response(
                    {'error': f'Stock insuficiente. Disponible: {product.stock}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Verificar si el item ya existe en el carrito
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': serializer.validated_data['quantity']}
            )
            
            if not created:
                # Si ya existe, actualizar cantidad
                cart_item.quantity += serializer.validated_data['quantity']
                cart_item.save()
            
            return Response(
                {
                    'message': 'Item agregado correctamente',
                    'item': CartItemSerializer(cart_item).data
                },
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
            )
            
        except Product.DoesNotExist:
            return Response(
                {'error': 'Producto no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )


class RemoveCartItemView(APIView):
    """
    DELETE: Eliminar item de un carrito
    """
    
    @remove_cart_item_decorator
    def delete(self, request, pk, item_id):
        cart = get_object_or_404(Cart, pk=pk)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        cart_item.delete()
        
        return Response(
            {'message': 'Item eliminado correctamente'},
            status=status.HTTP_204_NO_CONTENT
        )


class UpdateCartItemQuantityView(APIView):
    """
    PATCH: Actualizar cantidad de un item en el carrito
    """
    
    @update_cart_item_quantity_decorator
    def patch(self, request, pk, item_id):
        cart = get_object_or_404(Cart, pk=pk)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        quantity = request.data.get('quantity')
        
        if not quantity or int(quantity) < 1:
            return Response(
                {'error': 'La cantidad debe ser mayor a 0'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar stock
        if cart_item.product.stock < int(quantity):
            return Response(
                {'error': f'Stock insuficiente. Disponible: {cart_item.product.stock}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cart_item.quantity = int(quantity)
        cart_item.save()
        
        return Response(
            {
                'message': 'Cantidad actualizada correctamente',
                'item': CartItemSerializer(cart_item).data
            },
            status=status.HTTP_200_OK
        )
        

class CreateCartView(APIView):
    """
    POST: Crear un carrito vacío
    """
    
    @create_Cart
    def post(self, request):
        # Crear carrito vacío
        cart = Cart.objects.create(is_saved=False)
        serializer = CartSerializer(cart)
        
        return Response(
            {
                'message': 'Carrito creado correctamente',
                'cart': serializer.data
            },
            status=status.HTTP_201_CREATED
        )
