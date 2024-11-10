from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from decimal import Decimal
class Menu(models.Model):
    CATEGORY_CHOICES = [
        ('appetizer', 'Appetizer'),
        ('main_course', 'Main Course'),
        ('dessert', 'Dessert'),
        ('beverage', 'Beverage'),
    ]

    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    inventory = models.IntegerField()
    image = models.ImageField(upload_to='img_upload/', default='menu_images/default_image.png')  # Allow null/blank for existing items
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, null=True, blank=True)
    dish_of_the_day = models.BooleanField(default=False)  # Allow null/blank

    def __str__(self):
        return f'{self.title} : {self.inventory}'

class Booking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(default='placeholder@example.com')  # Placeholder email
    date = models.DateField(default=timezone.now)  # Default to current date
    time = models.TimeField(default=timezone.now)  # Default to current time
    guests = models.PositiveIntegerField(default=2)
    
    def __str__(self):
        return f"{self.name} - {self.date} {self.time}"


class DishOfTheDay(models.Model):
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.menu_item.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_cost(self):
        return sum(item.total_price for item in self.items.all())

    def __str__(self):
        return f"Cart of {self.user}" if self.user else "Anonymous Cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.menu_item.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} of {self.menu_item.name}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    delivery_crew = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="delivery_orders", null=True, blank=True
    )
    status = models.BooleanField(default=False, db_index=True)  # Consider using choices for more clarity
    total = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'))
    date = models.DateField(auto_now_add=True, db_index=True)  # Set date automatically on creation

    def __str__(self):
        return f"Order #{self.id} - User: {self.user.username} - Status: {'Delivered' if self.status else 'Pending'}"

    def calculate_total(self):
        """Calculate total based on related OrderItems."""
        self.total = sum(item.quantity * item.price for item in self.order.all())
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    menuitem = models.ForeignKey('Menu', on_delete=models.CASCADE)  # Menu should be defined elsewhere
    quantity = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('order', 'menuitem')

    def __str__(self):
        return f"{self.quantity} x {self.menuitem} @ {self.price} each"

