# urls.py
from django.urls import path
from .views import ProductListView, RecommendationView, ProductDetailView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('recommendations/', RecommendationView.as_view(), name='recommendations'),
]
