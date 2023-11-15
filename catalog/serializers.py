from .models import Product, Category, ProductCategory
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    
    class Meta:
        model = Category
        fields = ['id','name','image']
        
    def create(self, validated_data):
        print('validated_data', validated_data)
        category = Category.objects.create(name=validated_data['name'])
        if 'parent' in validated_data:
            category.parent = Category.objects.get(name=validated_data['parent'])
        return category
        
class ProductCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    
    class Meta:
        model = ProductCategory
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    
    class Meta:
        model = Product
        fields = "__all__"
        
    def create(self, validated_data):
        print('validated_data', validated_data)
        product = Product.objects.create(name=validated_data['name'])
        for cate in validated_data.pop('category'):
            category = Category.objects.get(name=cate['name'])
            ProductCategory.objects.create(product=product, category=category)
        return product
    
    def update(self, instance, validated_data): 
        print(instance)
        print('validated_data', validated_data)
        categories = ProductCategory.objects.filter(product=instance)
        if categories:
            categories.delete()
                
        instance.name = validated_data.get('name')
        for cate in validated_data.pop('category'):
            category = Category.objects.get(name=cate['name'])
            ProductCategory.objects.create(product=instance, category=category)        
        
        return instance