from rest_framework import generics, viewsets
from .models import Menu, Booking
from .serializers import MenuItemSerializer, BookingSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MenuForm,BookingForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .serializers import UserSerializer
from django.contrib.auth.forms import UserCreationForm

class MenuItemsView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Menu.objects.all()
    serializer_class = MenuItemSerializer

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):  # Use this to combine Retrieve, Update, and Destroy
    permission_classes = [IsAuthenticated]
    queryset = Menu.objects.all()
    serializer_class = MenuItemSerializer

class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Booking.objects.all()  # Fetch all booking objects
    serializer_class = BookingSerializer

def menu(request):
    menu_items = Menu.objects.all()  # Get all menu items
    categories = menu_items.values('category').distinct()  # Get distinct categories
    return render(request, 'menu.html', {'menu_items': menu_items, 'categories': categories})


def add_menu_item(request):
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)  # Include FILES to handle image uploads
        if form.is_valid():
            form.save()
            return redirect('menu')  # Redirect to the menu page or wherever you want
    else:
        form = MenuForm()
    
    return render(request, 'add_menu_item.html', {'form': form})

@login_required
def book_table(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            # Redirect to a confirmation page or render a success message
            return render(request, 'booking_success.html', {'reservation': reservation})
    else:
        form = BookingForm()
    return render(request, 'booking.html', {'form': form})

def menu_item_detail(request, pk):
    # Retrieve the specific menu item by its primary key (pk)
    menu_item = get_object_or_404(Menu, pk=pk)
    return render(request, 'menu_item_detail.html', {'menu_item': menu_item})

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def login_view(request):
    """Handle user login."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Change to your desired redirect page
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def logout_view(request):
    """Handle user logout."""
    logout(request)
    return redirect('home')

def register(request):
    """Handle user registration."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Log the user in immediately after registration
            # Redirect to the success page with user's information
            return render(request, 'registration_success.html', {
                'username': user.username,
                'user_id': user.id
            })
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]