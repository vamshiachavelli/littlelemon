from rest_framework import serializers
from .models import Menu, Booking

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'  # or specify fields like ['id', 'name', 'price']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking  # Use the actual name of your booking model
        fields = '__all__'  # This includes all fields in the Booking model
