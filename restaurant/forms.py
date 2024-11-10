from django import forms
from .models import Menu, Booking
from django.contrib.auth.models import Group, Permission, User

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['title', 'price', 'inventory', 'image', 'category']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'email', 'date', 'time', 'guests']

class GroupCreationForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']

class DeliveryCrewAssignmentForm(forms.Form):
    delivery_crew = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='Delivery Crew'), label='Delivery Crew')
