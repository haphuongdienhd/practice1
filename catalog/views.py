# products/views.py

from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from django.db.models import Count, F, Value

import requests

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer

from practice1.pagination import CustomPagination

from .models import Category, Product, Comment, ProductCategory, ProductImage
from .forms import CommentForm, ImageForm, ProductForm, CategoryForm
from .serializers import ProductSerializer, CategorySerializer

# Create your views here.

DEFAULT_URL = 'http://127.0.0.1:8000'

# Sub Function

def find_product_by_id(id):
    
    try:
        return Product.objects.get(id=id)
    except Product.DoesNotExist:
        return None

def find_product_by_name(name):
    
    try:
        return Product.objects.get(name=name)
    except Product.DoesNotExist:
        return None

def find_category_by_id(id):
    
    try:
        return Category.objects.get(id=id)
    except Category.DoesNotExist:
        return None
    
def find_category_by_name(name):
    
    try:
        return Category.objects.get(name=name)
    except Category.DoesNotExist:
        return None    

# Create a product
@login_required(login_url='/account/login/')
def product_create(request):
    
    if request.method == "POST":
        
        form = ProductForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse("catalog:product_list"))
    else:
        form = ProductForm()
        
    categories = Category.objects.all().order_by('name')

    return render(request, "product/product_form.html", { "form": form, "categories": categories,})

# Update a single product
@login_required(login_url='/account/login/')
def product_update(request, pk):
    product_obj = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        print(request.POST)
        form = ProductForm(request.POST,instance=product_obj, files=request.FILES)
        print(form.data)
        if form.is_valid():
            form.save()
            return redirect(reverse("catalog:product_detail", args=[pk,]))
        else: return HttpResponseNotFound(form.errors.as_data())
    else:
        form = ProductForm(instance=product_obj)
    
    categories = Category.objects.all().order_by('name')

    return render(request, "product/product_form.html", { "form": form, "object": product_obj, "categories": categories,})


# Delete a single product
@login_required(login_url='/account/login/')
def product_delete(request, pk):
    product_obj = get_object_or_404(Product, pk=pk)
    product_obj.delete()
    return redirect(reverse("catalog:product_list"))

# Create a category
@login_required(login_url='/account/login/')
def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse("catalog:category_list"))
    else:
        form = CategoryForm()

    return render(request, "category/category_form.html", { "form": form, })


# Retrieve category list
def category_list(request):
    categories = Category.objects.all().order_by('name')
    paginator = Paginator(categories, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "category/category_list.html", {"page_obj": page_obj})


# Retrieve a single category
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, "category/category_detail.html", { "category": category, })


# Update a single category
@login_required(login_url='/account/login/')
def category_update(request, pk):
    
    category_obj = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST,instance=category_obj, files=request.FILES)
        if form.is_valid():
            form.save()
        return redirect(reverse("catalog:category_detail", args=[pk,]))
    else:
        form = CategoryForm(instance=category_obj)

    return render(request, "category/category_form.html", { "form": form, "object": category_obj})


# Delete a single category
@login_required(login_url='/account/login/')
def category_delete(request, pk):
    category_obj = get_object_or_404(Category, pk=pk)
    category_obj.delete()
    return redirect(reverse("catalog:category_list"))

#API DRF
class ProductListApiView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by('-id')
    # renderer_classes = [TemplateHTMLRenderer,JSONRenderer]
    # template_name = 'product/product_list.html'
    pagination = CustomPagination()
    
    # 1. List all    
    def get(self, request, *args, **kwargs):
        # print("stillALIE", request.user.auth_token)
        products = Product.objects.all().order_by('-id').prefetch_related('category')
        if not request.GET.get('page'):
        
            # print("else")
            if not request.GET._mutable:
                request.GET._mutable = True

            # now you can edit it
            request.GET['page'] = 1
            
        page = self.pagination.paginate_queryset(products, request)
        serializer = ProductSerializer(page, many=True)
            
        return self.pagination.get_paginated_response(data=serializer.data)
    
    
    def post(self, request, *args, **kwargs):
        # print("request.data",request.data)
        
        if find_product_by_name(request.data['name']):
            return Response(
                {"message": f"Product with name {request.data['name']} already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if 'category' in request.data:
            for category in request.data['category']:
                if not find_category_by_name(category['name']):
                    return Response(
                    {"message": f"Category with name {category['name']} does not exist"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
        serializer = ProductSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductDetailApiView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by('-id')
    
    def get(self, request, pk, *args, **kwargs):
        product = find_product_by_id(pk)
        
        if product:
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(
                {"message": "Product with id %d does not exist" %(pk)},
                status=status.HTTP_404_NOT_FOUND
            )    
        
    def put(self, request, pk, *args, **kwargs):
        product = find_product_by_id(pk)
        # print(request)
        if not product:
            return Response(
                {"message": "Product with id %d does not exist" %(pk)}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        if 'name' not in request.data: 
            return Response({"message": "Missing name field"}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'category' in request.data:
            for category in request.data['category']:
                if not find_category_by_name(category['name']):
                    return Response(
                    {"message": f"Category with name {category['name']} does not exist"},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response({"message": "Missing category field"}, status=status.HTTP_400_BAD_REQUEST)
                
        serializer = ProductSerializer(instance=product,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk, *args, **kwargs):
        product = find_product_by_id(pk)
        # print(request)
        if not product:
            return Response(
                {"message": "Product with id %d does not exist" %(pk)}, 
                status=status.HTTP_404_NOT_FOUND
            )
        if 'category' in request.data:
            for category in request.data['category']:
                if not find_category_by_name(category['name']):
                    return Response(
                    {"message": f"Category with name {category['name']} does not exist"},
                    status=status.HTTP_404_NOT_FOUND
                )
                
        serializer = ProductSerializer(instance=product,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, *args, **kwargs):
        product = find_product_by_id(pk)
        
        if not product:
            return Response(
                {"message": "Product with id %d does not exist" %(pk)}, 
                status=status.HTTP_404_NOT_FOUND
            )
        product.delete()
        
        return Response(
            {"message": "Product deleted!"},
            status=status.HTTP_200_OK
        )
    
class CategoryListApiView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('-id')
    # renderer_classes = [TemplateHTMLRenderer,JSONRenderer]
    # template_name = 'category/category_list.html'
    pagination = CustomPagination()
    
    # 1. List all
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all().order_by('name')
        
        if not request.GET.get('page'):
            # print("else")
            if not request.GET._mutable:
                request.GET._mutable = True

            # now you can edit it
            request.GET['page'] = 1
            
        page = self.pagination.paginate_queryset(categories, request)
        # print(page)
        serializer = CategorySerializer(page, many=True)
        data = serializer.data
            
        return self.pagination.get_paginated_response(data=data)
    
    # 2. Create
    def post(self, request, *args, **kwargs):
        # print(request.data)
        if find_category_by_name(request.data['name']):
            return Response(
                {"message": f"Category with name {request.data['name']} already exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if 'parent' in request.data and not find_category_by_id(request.data['parent']):
            return Response(
                {"message": f"Category with id {request.data['parent']} does not exist"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = CategorySerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CategoryDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('-id')
    
    def get(self, request, pk, *args, **kwargs):
        category = find_category_by_id(pk)
        
        if category:
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(
                {"message": "Category with id %d does not exist" %(pk)},
                status=status.HTTP_404_NOT_FOUND
            )
        
                
    def put(self, request, pk, *args, **kwargs):
        category = find_category_by_id(pk)
        
        if not category:
            return Response(
                {"message": "Category with id %d does not exist" %(pk)}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        if 'name' not in request.data: 
            return Response({"message": "Missing name field"}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'parent' not in request.data: 
            return Response({"message": "Missing name parent"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if not find_category_by_id(request.data['parent']):
                return Response(
                    {"message": f"Category with id {request.data['parent']} does not exist"}, 
                    status=status.HTTP_404_NOT_FOUND
                )   
        
        serializer = CategorySerializer(instance=category,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk, *args, **kwargs):
        category = find_category_by_id(pk)
        if not category:
            return Response(
                {"message": "Category with id %d does not exist" %(pk)}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        if 'parent' in request.data:
            if not find_category_by_id(request.data['parent']):
                return Response(
                    {"message": f"Category with id {request.data['parent']} does not exist"}, 
                    status=status.HTTP_404_NOT_FOUND
                )   
        
        serializer = CategorySerializer(instance=category,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, *args, **kwargs):
        category = find_category_by_id(pk)
        if not category:
            return Response(
                {"message": "Category with id %d does not exist" %(pk)}, 
                status=status.HTTP_404_NOT_FOUND
            )
        category.delete()
        return Response(
            {"message": "Category deleted!"},
            status=status.HTTP_200_OK
        )
        
class ProductPerCateApiView(APIView):
    
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all().order_by('name').values('name').annotate(Count('product'))            
        return Response(categories, status=status.HTTP_200_OK)
    
# Product Image
@login_required(login_url='/account/login/')
def image_upload(request, pk):
    if request.method == 'POST':
        product = find_product_by_id(pk)
        form = ImageForm(request.POST, request.FILES)
        
        file = request.FILES['image']
        image = ProductImage.objects.create(image=file, product=product)
        image.save()
        # Get the current instance object to display in the template
        return render(request, 'product/product_detail.html', { "product": product, })
    else:        
        form = ImageForm()
        return render(request, 'product_image/upload.html', {'form': form,})
    
# Create comment
@login_required(login_url='/account/login/')
def create_comment(request, pk):
       
    if request.method == 'POST':        
        cf = CommentForm(request.POST or None)
        if cf.is_valid():
            product = find_product_by_id(pk)
            content = request.POST.get('content')
            comment = Comment.objects.create(product=product, user=request.user, content=content)
            comment.save()
            return render(request, 'product/product_detail.html', { "product": product, })
    else:
        cf = CommentForm()
        return render(request, 'comment/comment_form.html', {'comment_form':cf, })

# Comment list
def comment_list(request, pk):
    
    product = find_product_by_id(pk)
    comments = Comment.objects.filter(product=product)
    paginator = Paginator(comments, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "comment/comment_list.html", {"page_obj": page_obj, "product":product})

# Report total comments
class CommentPerProduct(APIView):
    
    def get(self, request, *args, **kwargs):
        
        products = Product.objects.all().order_by('-id').values('name').annotate(Count('comment'))            
        return Response(products, status=status.HTTP_200_OK)
    
# Retrieve product list
def product_list(request):
    if 'page' in request.GET:
        response = requests.get(f'{DEFAULT_URL}'+reverse('catalog:api_product_list')+f'?page={request.GET.get("page")}')
    else:
        response = requests.get(f'{DEFAULT_URL}'+reverse('catalog:api_product_list'))
    data = response.json()
        
    return render(request, "product/product_list.html", data)
    
# Retrieve a single product
def product_detail(request, pk):
    product_class = ProductDetailApiView()
    product = product_class.get(request,int(pk)).data
    return render(request, "product/product_detail.html", { "product": product, })