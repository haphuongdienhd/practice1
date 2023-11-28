from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class ProductTests(APITestCase):
    
    
    
    def test_create_product(self):
        url = reverse('api_category_list')
        