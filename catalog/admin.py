from django.utils.html import format_html
from django.contrib import admin
from .models import Product, Category, ProductCategory, ProductImage, Comment
# Register your models here.

    
class ProductCategoryAdmin(admin.ModelAdmin):    
    list_display = ['product', 'category']
    list_per_page = 10
    list_filter = ['product', 'category']
    search_fields = ['product__name','category__name']

class ProductCategoryInline(admin.TabularInline):    
    model=ProductCategory
    list_per_page = 10
    raw_id_fields=('category',)    

class ProductAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:192px; max-height:108px"/>'.format(obj.thumnail.url)) if obj.thumnail else None
    list_display = ['name', 'image_tag', 'list_category', 'total_comment']
    list_per_page = 10
    fieldsets = [
        ('Name', {'fields': ['name'],}),
        ('Thumnail', {'fields': ['thumnail'],}),
    ]
    list_filter = ['category']
    inlines=[ProductCategoryInline]
    search_fields = ['name']
    
    @admin.display(empty_value="???")
    def list_category(self, product):
        procates = ProductCategory.objects.filter(product=product)
        categories = ' '
        for cate in procates:
            categories += str(cate.category.name + ', ')
            
        return categories
    
    def total_comment(self, product):
        count = Comment.objects.filter(product=product).count()            
        return str(count)
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent','total_product']
    list_per_page = 10
    search_fields = ['name']    
    
    def total_product(self, category):
        count = ProductCategory.objects.filter(category=category).count()            
        return str(count)


class ProductImageAdmin(admin.ModelAdmin):
    
    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:192px; max-height:108px"/>'.format(obj.image.url))
    list_display = ['product','image_tag']
    list_per_page = 10
    list_filter = ['product']
    search_fields = ['product__name']
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user','product','content']
    list_per_page = 10
    fieldsets = [
        ('User', {'fields': ['user'],}),
        ('Product', {'fields': ['product'],}),
        ('Content', {'fields': ['content'],}),
    ]
    list_filter = ['user','product']
    search_fields = ['product__name','user__username']

admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductCategory,ProductCategoryAdmin)
admin.site.register(ProductImage,ProductImageAdmin)
admin.site.register(Comment,CommentAdmin)