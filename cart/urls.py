from django.urls import path
from .views import (
    SaveCartView,
    CartListView,
    CartDetailView,
    AddCartItemView,
    RemoveCartItemView,
    UpdateCartItemQuantityView,
    CreateCartView,
)

urlpatterns = [
    # Guardar carrito (endpoint principal para el frontend)
    path('cart/save/', SaveCartView.as_view(), name='save-cart'),
    
    # Listar y obtener carritos
    path('cart/', CartListView.as_view(), name='cart-list'),
    path('cart/<int:pk>/', CartDetailView.as_view(), name='cart-detail'),
    
    # Operaciones con items del carrito
    path('cart/<int:pk>/items/', AddCartItemView.as_view(), name='cart-add-item'),
    path('cart/<int:pk>/items/<int:item_id>/', RemoveCartItemView.as_view(), name='cart-remove-item'),
    path('cart/<int:pk>/items/<int:item_id>/quantity/', UpdateCartItemQuantityView.as_view(), name='cart-update-quantity'),
    path('cart/create/', CreateCartView.as_view(), name='cart-create'),
]