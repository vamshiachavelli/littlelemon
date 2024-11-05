from rest_framework import generics, viewsets
from .models import Menu, Booking, DishOfTheDay, Cart, CartItem
from .serializers import MenuItemSerializer, BookingSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MenuForm,BookingForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .serializers import UserSerializer
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.urls import reverse

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
    dish_of_the_day = Menu.objects.filter(dish_of_the_day=True).first()
    return render(request, 'menu.html', {'menu_items': menu_items, 'categories': categories, 'dish_of_the_day': dish_of_the_day})


def add_menu_item(request):
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)  # Include FILES to handle image uploads
        if form.is_valid():
            menu_item = form.save()  # Save the menu item and capture the instance
            return render(request, 'add_menu_item.html', {
                'form': MenuForm(),  # Reset the form for a new entry
                'menu_item': menu_item  # Pass the newly created item to the template
            })
    else:
        form = MenuForm()

    return render(request, 'add_menu_item.html', {'form': form})

@login_required(login_url='/login/')
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
            next_url = request.POST.get('next') or 'home'  # Fallback URL
            return redirect(next_url)
            #return redirect('home')  # Change to your desired redirect page
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def logout_view(request):
    """Handle user logout."""
    logout(request)
    return redirect('home')

from django.contrib.auth import get_user_model
from django.contrib import messages

def register(request):
    """Handle user registration."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Log the user in immediately after registration
            messages.success(request, f"User {user.username} registered successfully.")
            return redirect(reverse('home'))  # Redirect to the home page
        else:
            # Log or display form errors for debugging
            print("Form errors:", form.errors)
            messages.error(request, "There was an error in your registration form.")
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})


def registration_success(request, user_id):
    """Display the registration success page with user details."""
    user = get_object_or_404(User, id=user_id)  # Retrieve the user by ID
    return render(request, 'registration_success.html', {
        'username': user.username,  # Get the username from the user object
        'user_id': user.id  # Get the user ID
    })
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

def user_list_view(request):
    """Retrieve all users and render to an HTML template."""
    if request.user.is_authenticated:  # Ensure the user is logged in
        users = User.objects.all()  # Retrieve all users
        return render(request, 'user_list.html', {'users': users})
    else:
        return render(request, 'login.html', {'error': 'You must be logged in to view this page.'})
    

def set_dish_of_the_day(request):
    if request.method == "POST":
        dish_id = request.POST.get('dish_id')
        if dish_id:
            # Add dish to DishOfTheDay
            menu_item = Menu.objects.get(id=dish_id)
            DishOfTheDay.objects.get_or_create(menu_item=menu_item)

    # Remove dish if requested
    remove_id = request.POST.get('remove_id')
    if remove_id:
        DishOfTheDay.objects.filter(menu_item_id=remove_id).delete()

    menu_items = Menu.objects.all()
    dishes_of_the_day = DishOfTheDay.objects.all()
    
    return render(request, 'set_dish_of_the_day.html', {
        'menu_items': menu_items,
        'dishes_of_the_day': dishes_of_the_day
    })

def dish_of_the_day(request):
    # Retrieve all menu items marked as "dish of the day"
    dishes_of_the_day = Menu.objects.filter(dish_of_the_day=True)

    if request.method == 'POST':
        # Handle removal of the dish from the dish of the day
        remove_id = request.POST.get('remove_id')
        if remove_id:
            try:
                # Find the menu item and set dish_of_the_day to False
                menu_item = Menu.objects.get(id=remove_id)
                menu_item.dish_of_the_day = False
                menu_item.save()
            except Menu.DoesNotExist:
                pass  # Handle the case where the item does not exist

        # Redirect to the same view to refresh the list
        return redirect('dish_of_the_day')  # Use the name of the URL pattern for the view

    return render(request, 'dish_of_the_day.html', {'dishes_of_the_day': dishes_of_the_day})


def toggle_dish_of_the_day(request, item_id):
    if request.user.is_superuser:
        menu_item = Menu.objects.get(id=item_id)
        menu_item.dish_of_the_day = not menu_item.dish_of_the_day  # Toggle the status
        menu_item.save()
    return redirect('menu')  # Redirect to your menu page

@login_required
def add_to_cart(request, item_id):
    """Add the specified item to the cart with the given quantity."""
    cart = request.user.cart  # Assuming each user has a Cart model linked to them
    item = get_object_or_404(Menu, id=item_id)

    if request.method == "POST":
        quantity = request.POST.get("quantity", 1)

        # Ensure quantity is an integer and default to 1 if not
        try:
            quantity = int(quantity)
            if quantity < 1:  # Ensure quantity is at least 1
                quantity = 1
        except ValueError:
            quantity = 1

        # Update or create the cart item
        cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=item)
        
        # Set the quantity directly instead of incrementing
        cart_item.quantity = quantity  # This sets the quantity to the submitted value
        cart_item.save()

    return redirect('cart_detail')  # Redirect to the cart detail page or wherever needed



@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart_detail.html', {'cart': cart})

@login_required
def remove_from_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, menu_item_id=item_id)
    cart_item.delete()
    return redirect('cart_detail')

from django.http import HttpResponseBadRequest

@login_required
def update_cart_quantity(request, item_id):
    """Handle incrementing or decrementing the cart quantity for a specific item."""
    cart = request.user.cart  # Assuming each user has a Cart model linked to them
    item = get_object_or_404(Menu, id=item_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=item)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "increment":
            cart_item.quantity += 1  # Increment the quantity
            cart_item.save()
        elif action == "decrement":
            if cart_item.quantity > 1:  # Prevent going to negative quantity
                cart_item.quantity -= 1  # Decrement the quantity
                cart_item.save()
            else:
                cart_item.delete()  # Remove the item from the cart if quantity is 0

    return redirect('cart_detail')  # Redirect to the cart detail page

def delete_menu_item(request, item_id):
    if request.method == 'POST':
        menu_item = get_object_or_404(Menu, id=item_id)
        menu_item.delete()  # Delete the item from the database
        return redirect('menu')  # Redirect to the menu page with a success message