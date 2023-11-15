from .models import Product, Category, ProductImage, Comment
from django import forms

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = "__all__"
        
class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = "__all__"
        
 
class CommentForm(forms.ModelForm):
    content = forms.CharField(label ="", widget = forms.Textarea(
    attrs ={
        'class':'form-control',
        'placeholder':'Comment here !',
        'rows':4,
        'cols':50
    }))
    class Meta:
        model = Comment
        fields = ['content']
        
class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = ProductImage
        fields = ['image']