#product/api/views.py
from django.db.models import Count, F, Value

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from practice1.pagination import CustomPagination

from ..models import Category, Product, Comment, ProductCategory, ProductImage
from ..services import (
    create_category,
    find_category_by_id, 
    find_category_by_name,
    find_product_by_id,
    find_product_by_name,
)
from ..exceptions import *

from .serializers import ProductSerializer, CategorySerializer

class CategoryListApiView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('-id')
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
            return Response(
                {"exception": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ExceptionAlreadyExists as e:
            return Response(
                {"exception": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
class CategoryDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('-id')
    
    def get(self, request, pk, *args, **kwargs):
        try: 
            category = find_category_by_id(pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except ExceptionNotFound as e:
            return Response(
                {"exception": str(e)}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def put(self, request, pk, *args, **kwargs):
        try:
            category = find_category_by_id(pk)
                
            if 'name' not in request.data: 
                return Response({"exception": "Missing name field"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if Category.objects.filter(name=request.data['name']).exists():
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
            return Response(
                {"exception": str(e)}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except ExceptionAlreadyExists as e:
            return Response(
                {"exception": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def patch(self, request, pk, *args, **kwargs):
        try:
            category = find_category_by_id(pk)
            if Category.objects.filter(name=request.data['name']).exists():
                raise ObjectWithNameExists(CategoryObject(), request.data['name'])
            if 'parent' in request.data:
                find_category_by_id(request.data['parent'])
            
            serializer = CategorySerializer(instance=category,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except ExceptionNotFound as e:
            return Response(
                {"exception": str(e)}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except ExceptionAlreadyExists as e:
            return Response(
                {"exception": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def delete(self, request, pk, *args, **kwargs):
        try:
            category = find_category_by_id(pk)
            category.delete()
            return Response(
                {"message": "Category deleted!"},
                status=status.HTTP_204_NO_CONTENT
            )
        except ExceptionNotFound as e:
            return Response(
                {"exception": str(e)}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
class ProductListApiView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by('-id').prefetch_related('category')
    pagination = CustomPagination
    
    def post(self, request, *args, **kwargs):
        # print("request.data",request.data)
        try:
            if Product.objects.filter(name=request.data['name']).exists():
                raise ObjectWithNameExists(ProductObject(), request.data['name'])
            
            if 'category' in request.data:
                for category in request.data['category']:
                    find_category_by_name(category['name'])
                
            serializer = ProductSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except ExceptionNotFound as e:
            return Response(
                    {"exceptrion": str(e)},
                    status=status.HTTP_404_NOT_FOUND
                )   
            
        except ExceptionAlreadyExists as e:
            return Response(
                {"exception": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
class ProductDetailApiView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by('-id')
    
    def get(self, request, pk, *args, **kwargs):
        try:
            product = find_product_by_id(pk)            
            if product:
                serializer = ProductSerializer(product)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except ExceptionNotFound as e:
            return Response(
                    {"exceptrion": str(e)},
                    status=status.HTTP_404_NOT_FOUND
                )   
        
    def put(self, request, pk, *args, **kwargs):
        try:
            product = find_product_by_id(pk)
                
            if 'name' not in request.data: 
                return Response({"exception": "Missing name field"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if Product.objects.filter(name=request.data['name']).exists():
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
            return Response(
                    {"exception": str(e)},
                    status=status.HTTP_404_NOT_FOUND
                )
        except ExceptionAlreadyExists as e:
            return Response(
                {"exception": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
    def patch(self, request, pk, *args, **kwargs):
        try: 
            product = find_product_by_id(pk)
            if Product.objects.filter(name=request.data['name']).exists():
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
            return Response(
                    {"exception": str(e)},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        except ExceptionAlreadyExists as e:
            return Response(
                {"exception": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def delete(self, request, pk, *args, **kwargs):
        try:            
            product = find_product_by_id(pk)            
            product.delete()            
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )
        except ExceptionNotFound as e:
            return Response(
                {"exception": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )   
            
class ProductPerCateApiView(APIView):
    
    def get(self, request, *args, **kwargs):
        
        categories = Category.objects.all().order_by('name').values('name').annotate(Count('product'))   
                 
        return Response(categories, status=status.HTTP_200_OK)
    
class CommentPerProduct(APIView):
    
    def get(self, request, *args, **kwargs):        
        
        products = Product.objects.all().order_by('-id').values('name').annotate(Count('comment'))         
           
        return Response(products, status=status.HTTP_200_OK)