# products/views.py

from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Category, Product, Comment, ProductImage
from .forms import CommentForm, ImageForm, ProductForm, CategoryForm
from .exceptions import ExceptionNotFound, ExceptionAlreadyExists
from . import services


# Create your views here.

DEFAULT_URL = 'http://127.0.0.1:8000'
DEFAULT_PAGE_SIZE = 10

# Retrieve category list
def list_categories(request):
    categories = Category.objects.all().order_by('name')
    page_obj = services.paginate_list(list=categories, page_number=request.GET.get("page"), page_size=DEFAULT_PAGE_SIZE)    
    return render(request, "category/category_list.html", {"page_obj": page_obj})

# Create a category
@login_required(login_url='/account/login/')
def create_category(request):
    try:
        if request.method == "POST":
            
            if request.FILES:
                services.create_category(validate_data=request.POST, image=request.FILES["image"])
            else:
                services.create_category(validate_data=request.POST)
            return redirect(reverse("catalog:category_list"))
        else:
            form = CategoryForm()
            
        return render(request, "category/category_form.html", { "form": form, })
    
    except ExceptionNotFound as e:
        return e.return_404_http(e)
    except ExceptionAlreadyExists as e:
        return e.return_400_http(e)

# Retrieve a single category
def retrieve_category(request, pk):
    try:
        category = services.find_category_by_id(pk)
        return render(request, "category/category_detail.html", { "category": category, })
    except ExceptionNotFound as e:
        return e.return_404_http(e)

# Update a single category
@login_required(login_url='/account/login/')
def update_category(request, pk):
    try:
        category_obj = services.find_category_by_id(pk)
        if request.method == "POST":
            form = CategoryForm(request.POST,instance=category_obj, files=request.FILES)
            if form.is_valid():
                form.save()
            return redirect(reverse("catalog:category_detail", args=[pk,]))
        else:
            form = CategoryForm(instance=category_obj)

        return render(request, "category/category_form.html", { "form": form, "object": category_obj})
    except ExceptionNotFound as e:
        return e.return_404_http(e)
    except ExceptionAlreadyExists as e:
        return e.return_400_http(e)
# Delete a single category
@login_required(login_url='/account/login/')
def delete_category(request, pk):
    try:
        category_obj = services.find_category_by_id(pk)
        category_obj.delete()
        return redirect(reverse("catalog:category_list"))
    except ExceptionNotFound as e:
        e.return_404_http(e)

# Retrieve product list
def list_products(request):
    products = Product.objects.all().order_by('-id').prefetch_related('category')
    page_obj = services.paginate_list(list=products, page_number=request.GET.get("page"), page_size=DEFAULT_PAGE_SIZE)    
    return render(request, "product/product_list.html", {"page_obj": page_obj})
    
# Retrieve a single product
def retrieve_product(request, pk):
    try:
        product = services.find_product_by_id(pk)
        images = ProductImage.objects.select_related('product').filter(product=product)
        return render(request, "product/product_detail.html", { "product": product, 'images':images})
    except ExceptionNotFound as e:
        return e.return_404_http(e)

# Create a product
@login_required(login_url='/account/login/')
def create_product(request):    
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
def update_product(request, pk):
    try:
        product = services.find_product_by_id(pk)
        if request.method == 'POST':
            form = ProductForm(request.POST,instance=product, files=request.FILES)
            if form.is_valid():
                form.save()
                return redirect(reverse("catalog:product_detail", args=[pk,]))
            else: return HttpResponseNotFound(form.errors.as_data())
        else:
            form = ProductForm(instance=product)    
        categories = Category.objects.all().order_by('name')
        return render(request, "product/product_form.html", { "form": form, "object": product, "categories": categories,})
    except ExceptionNotFound as e:
        return e.return_404_http(e)

# Delete a single product
@login_required(login_url='/account/login/')
def delete_product(request, pk):
    try:
        product = services.find_product_by_id(pk)
        product.delete()
        return redirect(reverse("catalog:product_list"))
    except ExceptionNotFound as e:
        return e.return_404_http(e)

# Product Image
@login_required(login_url='/account/login/')
def upload_image(request, pk):
    try:
        if request.method == 'POST':
            product = services.find_product_by_id(pk)
            form = ImageForm(request.POST, request.FILES)
            
            file = request.FILES['image']
            image = ProductImage.objects.create(image=file, product=product)
            image.save()
            # Get the current instance object to display in the template
            images = ProductImage.objects.select_related('product').filter(product=product)
            return render(request, 'product/product_detail.html', { "product": product, 'images':images,})
        else:        
            form = ImageForm()
            return render(request, 'product_image/upload.html', {'form': form,})
    except ExceptionNotFound as e:
        return e.return_404_http(e)
        
# Create comment
@login_required(login_url='/account/login/')
def create_comment(request, pk):
    try:   
        if request.method == 'POST':        
            cf = CommentForm(request.POST or None)
            if cf.is_valid():
                product = services.find_product_by_id(pk)
                content = request.POST.get('content')
                comment = Comment.objects.create(product=product, user=request.user, content=content)
                comment.save()
                return render(request, 'product/product_detail.html', { "product": product, })
        else:
            cf = CommentForm()
            return render(request, 'comment/comment_form.html', {'comment_form':cf, })
    except ExceptionNotFound as e:
        return e.return_404_http(e)

# Comment list
def list_comment(request, pk):
    try: 
        product = services.find_product_by_id(pk)
        comments = Comment.objects.filter(product__pk=pk)
        page_obj = services.paginate_list(list=comments, page_number=request.GET.get("page"), page_size=DEFAULT_PAGE_SIZE)
        return render(request, "comment/comment_list.html", {"page_obj": page_obj, "product":product})
    except ExceptionNotFound as e:
        return e.return_404_http(e)