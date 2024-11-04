from django.db import models
from django.utils import timezone


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
