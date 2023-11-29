# products/api/urls.py

from django.urls import path
from . import views


urlpatterns = [    
    # API
    
    # Retrieve category list
    path('api/categories/', views.CategoryListApiView.as_view(), name="api_category_list"),
    
    # Detail category
    path('api/categories/<int:pk>/', views.CategoryDetailApiView.as_view(), name="api_category_detail"),
    
    # Retrieve product list
    path('api/products/', views.ProductListApiView.as_view(), name="api_product_list"),
    
    # Detail product
    path('api/products/<int:pk>/', views.ProductDetailApiView.as_view(), name="api_product_detail"),
    
    # Product per category
    path('api/products-per-category/', views.ProductPerCateApiView.as_view(), name='product_per_cate'),
    
    path('api/comments-per-product/', views.CommentPerProduct.as_view(), name='comment_per_product'),
]