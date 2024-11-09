from rest_framework import generics, viewsets
from .models import Menu, Booking, DishOfTheDay, Cart, CartItem
from .serializers import MenuItemSerializer, BookingSerializer, UserSerializer
from .forms import MenuForm,BookingForm, GroupCreationForm
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseBadRequest

# Function to check if the user is a manager
def is_manager(user):
    return user.groups.filter(name='manager').exists()

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
    """Display the menu page with cart quantities."""
    # For authenticated users, retrieve the cart associated with the user
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        cart_items = CartItem.objects.filter(cart=cart) if cart else []
        cart_item_ids = set(cart_items.values_list('menu_item_id', flat=True))  # Get ids of items in the cart
    else:
        # For anonymous users, use the session-based cart
        cart_id = request.session.get('cart_id', None)
        cart_items = []
        cart_item_ids = set()
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart_items = CartItem.objects.filter(cart=cart)
            cart_item_ids = set(cart_items.values_list('menu_item_id', flat=True))  # Get ids of items in the cart

    categories = Menu.objects.values('category').distinct()  # Get distinct categories
    menu_items = Menu.objects.all()  # Get all menu items
    return render(request, 'menu.html', {
        'menu_items': menu_items,
        'categories': categories,
        'cart_items': cart_items,  # Pass the cart items to the template
        'cart_item_ids': cart_item_ids,  # Pass the set of item ids that are in the cart
    })

@user_passes_test(is_manager or user.is_superuser)
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

@user_passes_test(is_manager or user.is_superuser)
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

from django.shortcuts import render

def add_to_cart(request, item_id):
    """Add the specified item to the cart with the given quantity."""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = request.session.get('cart_id', None)
        if not cart_id:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
        else:
            cart = Cart.objects.get(id=cart_id)

    item = get_object_or_404(Menu, id=item_id)

    if request.method == "POST":
        quantity = request.POST.get("quantity", 1)
        try:
            quantity = int(quantity)
            if quantity < 1:
                quantity = 1
        except ValueError:
            quantity = 1

        cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=item)

        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()

    # After updating the cart, pass the cart context to the menu page
    return redirect('menu')

def remove_from_cart(request, item_id):
    """Remove the specified item from the cart."""
    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user)
    else:
        cart_id = request.session.get('cart_id', None)
        if not cart_id:
            return redirect('cart_detail')  # If no cart exists for anonymous user, just redirect
        cart = get_object_or_404(Cart, id=cart_id)

    cart_item = get_object_or_404(CartItem, cart=cart, menu_item_id=item_id)
    cart_item.delete()

    # After removing the item, pass the updated cart context
    return redirect('cart_detail')


def cart_detail(request):
    # For authenticated users, retrieve the cart associated with the user
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        cart_id = request.session.get('cart_id', None)
        if not cart_id:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
        else:
            cart = Cart.objects.get(id=cart_id)

    return render(request, 'cart_detail.html', {'cart': cart})


def update_cart_quantity(request, item_id):
    """Handle incrementing or decrementing the cart quantity for a specific item."""
    # Handle authenticated users
    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user)
    else:
        # Handle anonymous users using session-based cart
        cart_id = request.session.get('cart_id', None)
        if not cart_id:
            return HttpResponseBadRequest("No cart found.")
        cart = get_object_or_404(Cart, id=cart_id)

    # Get the menu item
    item = get_object_or_404(Menu, id=item_id)

    # Get or create the cart item
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

@user_passes_test(is_manager or user.is_superuser)
def delete_menu_item(request, item_id):
    if request.method == 'POST':
        menu_item = get_object_or_404(Menu, id=item_id)
        menu_item.delete()  # Delete the item from the database
        return redirect('menu')  # Redirect to the menu page with a success message
    
#Group creation
@login_required
@user_passes_test(is_manager or user.is_superuser)
def create_group(request):
    if request.method == 'POST':
        form = GroupCreationForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.save()  # Save the group first
            form.cleaned_data['permissions'].update(group.permissions.all())
            return redirect('group_list')  # Redirect to a group list or dashboard
    else:
        form = GroupCreationForm()
    return render(request, 'create_group.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, Permission, User
from django.contrib.auth.decorators import user_passes_test
from django.contrib.contenttypes.models import ContentType

# Check if user is admin
@user_passes_test(is_manager or user.is_superuser)
def manage_groups(request):
    groups = Group.objects.all()
    return render(request, 'manage_groups.html', {'groups': groups})

'''@user_passes_test(is_manager or user.is_superuser)
def add_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('name')
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            permissions = request.POST.getlist('permissions')
            group.permissions.set(Permission.objects.filter(id__in=permissions))
        return redirect('manage_groups')
    permissions = Permission.objects.all()
    return render(request, 'add_group.html', {'permissions': permissions})'''

@user_passes_test(is_manager or user.is_superuser)
def group_detail(request, group_id):
    group = Group.objects.get(id=group_id)
    users = User.objects.exclude(groups=group)
    permissions = Permission.objects.all()

    if request.method == 'POST':
        if 'add_user' in request.POST:
            user_id = request.POST.get('user_id')
            user = User.objects.get(id=user_id)
            group.user_set.add(user)
        elif 'add_permission' in request.POST:
            perm_id = request.POST.get('perm_id')
            permission = Permission.objects.get(id=perm_id)
            group.permissions.add(permission)

    return render(request, 'group_detail.html', {
        'group': group,
        'users': users,
        'permissions': permissions
    })



@user_passes_test(is_manager or user.is_superuser)
def add_group(request):
    if request.method == "POST":
        form = GroupCreationForm(request.POST)
        if form.is_valid():
            group_name = form.cleaned_data['group_name']
            group = Group.objects.create(name=group_name)

            # Assign permissions to the group
            permissions = form.cleaned_data['permissions']
            for perm_id in permissions:
                permission = Permission.objects.get(id=perm_id)
                group.permissions.add(permission)

            return render(request, 'group_added.html', {'group': group})
    else:
        form = GroupCreationForm()
    return render(request, 'add_group.html', {'form': form})

@user_passes_test(is_manager or user.is_superuser)
def remove_user_from_group(request, group_id, user_id):
    group = Group.objects.get(id=group_id)
    user = User.objects.get(id=user_id)
    group.user_set.remove(user)
    return redirect('group_detail', group_id=group.id)

from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, Permission
from .models import User

def remove_permission_from_group(request, group_id, perm_id):
    group = Group.objects.get(id=group_id)
    permission = Permission.objects.get(id=perm_id)
    group.permissions.remove(permission)
    return redirect('group_detail', group_id=group.id)

def remove_user_from_group(request, group_id, user_id):
    group = Group.objects.get(id=group_id)
    user = User.objects.get(id=user_id)
    group.user_set.remove(user)
    return redirect('group_detail', group_id=group.id)
