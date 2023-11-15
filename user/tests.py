from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class AccountTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('api_register')
        data = {
            "username": "user1",
            "password": "Nhanma123456",
            "password2": "Nhanma123456",
            "email": "user1@example.com"
            }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'user1')
        
    def test_create_account_2(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('api_register')
        data = {
            "username": "user1",
            "password": "Nhanma123456",
            "password2": "Nhanma123456",
            "email": "user1@example.com"
            }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'user1')