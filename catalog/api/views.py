#product/api/views.py
from django.db.models import Count

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from practice1.pagination import CustomPagination

from ..models import Category, Product
from ..services import (
    create_category,
    create_product,
    find_category_by_id, 
    find_category_by_name,
    find_product_by_id,
)
from ..exceptions import *

from .serializers import ProductSerializer, CategorySerializer

class CategoryListApiView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('-id').select_related('parent')
    pagination_class = CustomPagination
    
    # 2. Create
    def post(self, request, *args, **kwargs):
        try:
            category = create_category(request.data)
            data = CategorySerializer(category, partial=True).data
            return Response(
                data,
                status=status.HTTP_201_CREATED
            )
        except ExceptionNotFound as e:
            return e.return_404_response(e)
        except ExceptionAlreadyExists as e:
            return e.return_400_response(e)
    
class CategoryDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('-id').select_related('parent')
    
    def get(self, request, pk, *args, **kwargs):
        try: 
            category = find_category_by_id(pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except ExceptionNotFound as e:
            return e.return_404_response(e)
    
    def put(self, request, pk, *args, **kwargs):
        try:
            category = find_category_by_id(pk)
                
            if 'name' not in request.data: 
                return Response({"exception": "Missing name field"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if category.name != request.data['name'] and Category.objects.filter(name=request.data['name']).exists():
                    raise ObjectWithNameExists(CategoryObject(), request.data['name'])
            
            if 'parent' not in request.data: 
                return Response({"exception": "Missing parent field"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                find_category_by_id(request.data['parent'])
            
            serializer = CategorySerializer(instance=category,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except ExceptionNotFound as e:
            return e.return_404_response(e)
        except ExceptionAlreadyExists as e:
            return e.return_400_response(e)
    
    def patch(self, request, pk, *args, **kwargs):
        try:
            category = find_category_by_id(pk)
            if category.name != request.data['name'] and Category.objects.filter(name=request.data['name']).exists():
                raise ObjectWithNameExists(CategoryObject(), request.data['name'])
            if 'parent' in request.data:
                find_category_by_id(request.data['parent'])
            
            serializer = CategorySerializer(instance=category,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except ExceptionNotFound as e:
            return e.return_404_response(e)
        except ExceptionAlreadyExists as e:
            return e.return_400_response(e)
    
    def delete(self, request, pk, *args, **kwargs):
        try:
            category = find_category_by_id(pk)
            category.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )
        except ExceptionNotFound as e:
            return e.return_404_response(e)
        
class ProductListApiView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.order_by('-id').prefetch_related('category__parent')
    pagination = CustomPagination
    
    def post(self, request, *args, **kwargs):
        try:
            product = create_product(request.data)                
            serializer = ProductSerializer(product, partial=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except ExceptionNotFound as e:
            return e.return_404_response(e)
            
        except ExceptionAlreadyExists as e:
            return e.return_400_response(e)
    
class ProductDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.order_by('-id').prefetch_related('category__parent')
    
    def get(self, request, pk, *args, **kwargs):
        try:
            product = find_product_by_id(pk)            
            if product:
                serializer = ProductSerializer(product)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except ExceptionNotFound as e:
            return e.return_404_response(e)
        
    def put(self, request, pk, *args, **kwargs):
        try:
            product = find_product_by_id(pk)
                
            if 'name' not in request.data: 
                return Response({"exception": "Missing name field"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if product.name != request.data['name'] and Product.objects.filter(name=request.data['name']).exists():
                    raise ObjectWithNameExists(ProductObject(), request.data['name'])
            
            if 'category' in request.data:
                for category in request.data['category']:
                    find_category_by_name(category['name'])
            else:
                return Response({"exception": "Missing category field"}, status=status.HTTP_400_BAD_REQUEST)
                    
            serializer = ProductSerializer(instance=product,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except ExceptionNotFound as e:
            return e.return_404_response(e)
        except ExceptionAlreadyExists as e:
            return e.return_400_response(e)
        
    def patch(self, request, pk, *args, **kwargs):
        try: 
            product = find_product_by_id(pk)
            if product.name != request.data['name'] and Product.objects.filter(name=request.data['name']).exists():
                raise ObjectWithNameExists(ProductObject(), request.data['name'])
            
            if 'category' in request.data:
                for category in request.data['category']:
                    find_category_by_name(category['name'])
                    
            serializer = ProductSerializer(instance=product,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except ExceptionNotFound as e:
            return e.return_404_response(e)
        
        except ExceptionAlreadyExists as e:
            return e.return_400_response(e)
    
    def delete(self, request, pk, *args, **kwargs):
        try:            
            product = find_product_by_id(pk)            
            product.delete()            
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )
        except ExceptionNotFound as e:
            return e.return_404_response(e)  
            
class ProductPerCateApiView(APIView):
    
    def get(self, request, *args, **kwargs):
        
        categories = Category.objects.all().order_by('name').values('name').annotate(Count('product'))   
                 
        return Response(categories, status=status.HTTP_200_OK)
    
class CommentPerProduct(APIView):
    
    def get(self, request, *args, **kwargs):        
        
        products = Product.objects.all().order_by('-id').values('name').annotate(Count('comment'))         
           
        return Response(products, status=status.HTTP_200_OK)
