from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    parent = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, blank=True, related_name='parent_category')
    image = models.ImageField(upload_to='images/%Y/%m/%d/', null=True, blank=True)
    
    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse('catalog:category_list')
    
    
class Product(models.Model):
    name = models.CharField(max_length=80, unique=True)
    thumnail = models.ImageField(upload_to='images/%Y/%m/%d/', null=True, blank=True)
    category = models.ManyToManyField(Category, through="ProductCategory",blank=True,)
    
    def __str__(self):
        return str(self.name)
    
class ProductCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
class ProductImage(models.Model):
    image = models.ImageField(upload_to='images/%Y/%m/%d/', blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.CharField(max_length=240, unique=False)