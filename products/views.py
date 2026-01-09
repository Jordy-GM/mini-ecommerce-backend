from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Product
from .serializers import ProductSerializer

# Importar decoradores de documentación
from docs.decorators.swagger_decorators import (
    product_list_decorator,
    product_detail_decorator,
    product_active_decorator,
)


class ProductListView(APIView):
    """
    GET: Listar todos los productos activos
    """
    
    @product_list_decorator
    def get(self, request):
        products = Product.objects.filter(is_active=True)
        
        # Filtros opcionales
        search = request.query_params.get('search', None)
        if search:
            products = products.filter(name__icontains=search)
        
        ordering = request.query_params.get('ordering', '-created_at')
        products = products.order_by(ordering)
        
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    """
    GET: Obtener detalles de un producto específico
    """
    
    @product_detail_decorator
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk, is_active=True)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductActiveView(APIView):
    """
    GET: Obtener productos activos con stock disponible
    """
    
    @product_active_decorator
    def get(self, request):
        products = Product.objects.filter(is_active=True, stock__gt=0)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)