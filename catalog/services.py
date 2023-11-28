#catalog/services.py

from django.core.paginator import Paginator

from .exceptions import *
from .models import Product, Category

def find_category_by_id(id):
    """Return object or raise string exceptions"""
    try:
        return Category.objects.get(id=id)
    except Category.DoesNotExist:
        raise ObjectNotFoundById(CategoryObject(), id)
    
def find_category_by_name(name):
    """Return object or raise string exceptions"""
    try:
        return Category.objects.get(name=name)
    except Category.DoesNotExist:
        raise ObjectNotFoundByName(CategoryObject(), name)
    
def find_product_by_id(id):
    """Return object or raise string exceptions"""
    try:
        return Product.objects.get(id=id)
    except Product.DoesNotExist:
        raise ObjectNotFoundById(ProductObject(), id)

def find_product_by_name(name):
    """Return object or raise string exceptions"""
    try:
        return Product.objects.get(name=name)
    except Product.DoesNotExist:
        raise ObjectNotFoundByName(ProductObject(), name)
    
def create_category(validate_data, **kwargs) -> Category:
    name = validate_data['name']    
    if Category.objects.filter(name=name).exists():
        raise ObjectWithNameExists(CategoryObject(), name)
    
    if 'parent' in validate_data:
        parent = validate_data['parent'] or None      
        if parent:
            find_category_by_id(parent)
    else:
        parent = None
        
    category = Category.objects.create(name=name,parent=parent,**kwargs)
    category.save()
    return category

def create_product(validate_data, **kwargs) -> Product:
    try:
        print(validate_data)
        name = validate_data['name']
        if Product.objects.filter(name=name).exists():
            raise ObjectWithNameExists(ProductObject(), name)
                
        product = Product.objects.create(name=name,**kwargs)
        
        if 'category' in validate_data:
            for category in validate_data['category']:
                product.category.add(find_category_by_name(category['name'])) if 'name' in category else product.category.add(find_category_by_id(category))
        
        product.save()
        return product
    except Exception as e:
        print("aosidpar")
        product.delete()
        raise e

def paginate_list(list, page_number, page_size):
    """Return list object at page_number"""
    paginator = Paginator(list, page_size)
    page_obj = paginator.get_page(page_number)
    
    return page_obj