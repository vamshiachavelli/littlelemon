from django import forms
from .models import Menu, Booking

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['title', 'price', 'inventory', 'image', 'category']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'email', 'date', 'time', 'guests']
