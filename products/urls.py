from django.urls import path
from .views import ProductListView, ProductDetailView, ProductActiveView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/active/', ProductActiveView.as_view(), name='product-active'),
]