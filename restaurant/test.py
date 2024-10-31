# tests/test_views.py
from django.test import TestCase
from django.urls import reverse
from .models import Menu
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

class MenuViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Create a few menu items
        Menu.objects.create(title="Falafel Platter", price=9.28, inventory=10)
        Menu.objects.create(title="Chicken Over Rice", price=10.98, inventory=15)

        # Authenticate the user
        self.client.login(username='testuser', password='testpassword')

    def test_get_all_menus(self):
        # Make the request as an authenticated user
        response = self.client.get(reverse('menu-items'))

        # Expected data to match the serialized response
        expected_data = [
            {'id': 1, 'title': "Falafel Platter", 'price': "9.28", 'inventory': 10},
            {'id': 2, 'title': "Chicken Over Rice", 'price': "10.98", 'inventory': 15}
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_data)
