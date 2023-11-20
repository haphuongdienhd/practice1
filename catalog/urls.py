# products/urls.py

from django.urls import path, re_path
from . import views

# namespace
app_name = 'catalog'

urlpatterns = [

    # Create a product
    path('products/create/', views.product_create, name='product_create'),

    # Retrieve product list
    path('products/', views.product_list, name='product_list'),

    # Retrieve single product object
    re_path(r'^products/(?P<pk>\d+)/$', views.product_detail, name='product_detail'),

    # Update a product
    re_path(r'^products/(?P<pk>\d+)/update/$', views.product_update, name='product_update'),

    # Delete a product
    re_path(r'^products/(?P<pk>\d+)/delete/$', views.product_delete, name='product_delete'),
    
    # Product Image
    re_path(r'^products/(?P<pk>\d+)/upload/$', views.image_upload, name='image_upload'),
    
    # Comment on Product
    re_path(r'^products/(?P<pk>\d+)/comments/create$', views.create_comment, name='comment_form'),
    re_path(r'^products/(?P<pk>\d+)/comments/$', views.comment_list, name='comment_list'),
    re_path(r'^api/comments-per-product/$', views.CommentPerProduct.as_view(), name='comment_per_product'),
    
    # Create a category
    path('categories/create/', views.category_create, name='category_create'),

    # Retrieve category list
    path('categories/', views.category_list, name='category_list'),

    # Retrieve single category object
    re_path(r'^categories/(?P<pk>\d+)/$', views.category_detail, name='category_detail'),

    # Update a category
    re_path(r'^categories/(?P<pk>\d+)/update/$', views.category_update, name='category_update'),

    # Delete a category
    re_path(r'^categories/(?P<pk>\d+)/delete/$', views.category_delete, name='category_delete'),

    # API
    # Retrieve product list
    path('api/products/', views.ProductListApiView.as_view(), name="api_product_list"),
    
    # Detail product
    path('api/products/<int:pk>/', views.ProductDetailApiView.as_view(), name="api_product_detail"),
    
    # Retrieve category list
    path('api/categories/', views.CategoryListApiView.as_view(), name="api_category_list"),
    
    # Detail category
    path('api/categories/<int:pk>/', views.CategoryDetailApiView.as_view(), name="api_category_detail"),
    
    # Product per category
    path('api/products-per-category/', views.ProductPerCateApiView.as_view(), name='product_per_cate'),
    
]