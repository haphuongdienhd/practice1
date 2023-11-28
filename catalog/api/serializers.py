from ..models import Product, Category, ProductCategory
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False) 
    
    class Meta:
        model = Category
        fields = '__all__'
        
    def get_fields(self):
        fields = super(CategorySerializer, self).get_fields()
        fields['parent'] = CategorySerializer(required=False)
        return fields
                        
    def create(self, validated_data):
        category = Category.objects.create(name=validated_data['name'])
        if 'parent' in validated_data:
            category.parent = Category.objects.get(id=validated_data['parent'])
        return category
    
    def update(self, instance, validated_data): 
        
        if 'parent' in validated_data:
            instance.parent = validated_data.get('parent')
        if 'name' in validated_data:
            instance.name = validated_data.get('name')
        instance.save()
        return instance
        
class ProductCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    
    class Meta:
        model = ProductCategory
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    category = CategorySerializer(many=True,required=False)
    
    class Meta:
        model = Product
        fields = "__all__"
        
        
    def create(self, validated_data):
        product = Product.objects.create(name=validated_data['name'])
        if 'category' in validated_data:
            for cate in validated_data.pop('category'):
                category = Category.objects.get(name=cate['name'])
                ProductCategory.objects.create(product=product, category=category)
        return product
    
    def update(self, instance, validated_data):        
        if 'category' in validated_data:
            categories = ProductCategory.objects.filter(product=instance)
            if categories:
                categories.delete()
            for cate in validated_data.pop('category'):
                category = Category.objects.get(name=cate['name'])
                ProductCategory.objects.create(product=instance, category=category)        
        if 'name' in validated_data:
            instance.name = validated_data.get('name')
            instance.save()
        
        return instance