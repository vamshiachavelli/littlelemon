from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Menu, Booking
from .serializers import MenuItemSerializer, BookingSerializer

class MenuViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.menu_item = Menu.objects.create(name='Test Dish', description='A delicious test dish', price=9.99, category='Main Course')

    def test_menu_items_list_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('menu-items'))  # Assuming the URL is named 'menu-items'
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.menu_item.name)

    def test_menu_items_create_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('menu-items'), {
            'name': 'New Dish',
            'description': 'A new delicious dish',
            'price': 12.99,
            'category': 'Main Course',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 2)

    def test_menu_items_create_unauthenticated(self):
        response = self.client.post(reverse('menu-items'), {
            'name': 'Unauthorized Dish',
            'description': 'An unauthorized dish',
            'price': 9.99,
            'category': 'Appetizer',
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class BookingViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_booking_create_authenticated(self):
        response = self.client.post(reverse('booking-list'), {
            'user': self.user.id,
            'date': '2024-12-01T19:00:00Z',
            'num_people': 4,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)

    def test_booking_create_unauthenticated(self):
        self.client.logout()
        response = self.client.post(reverse('booking-list'), {
            'user': self.user.id,
            'date': '2024-12-01T19:00:00Z',
            'num_people': 4,
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class UserAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_login_success(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword',
        })
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Redirect after login

    def test_login_fail(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Stay on the login page
        self.assertContains(response, 'Invalid credentials')

    def test_register_user(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Registration page, can redirect later

class MenuItemDetailViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.menu_item = Menu.objects.create(name='Test Dish', description='A delicious test dish', price=9.99, category='Main Course')

    def test_menu_item_detail_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('menu_item_detail', args=[self.menu_item.pk]))  # Replace with the actual URL name
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.menu_item.name)

    def test_menu_item_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('menu_item_detail', args=[self.menu_item.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

