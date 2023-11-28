# products/urls.py

from django.urls import include, path, re_path

from catalog.api import urls as apiurls
from . import views

# namespace
app_name = 'catalog'

urlpatterns = [
    
    # Create a category
    path('categories/create/', views.create_category, name='category_create'),

    # Retrieve category list
    path('categories/', views.list_categories, name='category_list'),

    # Retrieve single category object
    re_path(r'^categories/(?P<pk>\d+)/$', views.retrieve_category, name='category_detail'),

    # Update a category
    re_path(r'^categories/(?P<pk>\d+)/update/$', views.update_category, name='category_update'),

    # Delete a category
    re_path(r'^categories/(?P<pk>\d+)/delete/$', views.delete_category, name='category_delete'),

    # Create a product
    path('products/create/', views.create_product, name='product_create'),

    # Retrieve product list
    path('products/', views.list_products, name='product_list'),

    # Retrieve single product object
    re_path(r'^products/(?P<pk>\d+)/$', views.retrieve_product, name='product_detail'),

    # Update a product
    re_path(r'^products/(?P<pk>\d+)/update/$', views.update_product, name='product_update'),

    # Delete a product
    re_path(r'^products/(?P<pk>\d+)/delete/$', views.delete_product, name='product_delete'),
    
    # Product Image
    re_path(r'^products/(?P<pk>\d+)/upload/$', views.upload_image, name='image_upload'),
    
    # Comment on Product
    re_path(r'^products/(?P<pk>\d+)/comments/create$', views.create_comment, name='comment_form'),
    
    re_path(r'^products/(?P<pk>\d+)/comments/$', views.list_comment, name='comment_list'),   
        
]

urlpatterns += apiurls.urlpatterns