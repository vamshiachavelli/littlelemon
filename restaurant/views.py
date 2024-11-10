from rest_framework import generics, viewsets
from .models import Menu, Booking, DishOfTheDay, Cart, CartItem, Order, OrderItem
from .serializers import MenuItemSerializer, BookingSerializer, UserSerializer
from .forms import MenuForm,BookingForm, GroupCreationForm, DeliveryCrewAssignmentForm
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseBadRequest, Http404, HttpResponse
from django.contrib import messages
from decimal import Decimal
import datetime


def is_superuser_or_groups(user, group_names):
    return user.is_superuser or user.groups.filter(name__in=group_names).exists()

def superuser_or_multiple_groups_required(group_names):
    def decorator(view_func):
        return user_passes_test(lambda u: is_superuser_or_groups(u, group_names))(view_func)
    return decorator


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


from django.shortcuts import render
from .models import Cart, CartItem, Menu

def menu(request):
    """Display the menu page with cart quantities."""
    # For authenticated users, retrieve the cart associated with the user
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        cart_items = CartItem.objects.filter(cart=cart) if cart else CartItem.objects.none()
        cart_item_ids = set(cart_items.values_list('menu_item_id', flat=True))  # Get ids of items in the cart
    else:
        # For anonymous users, use the session-based cart
        cart_id = request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.filter(id=cart_id).first()
            cart_items = CartItem.objects.filter(cart=cart) if cart else CartItem.objects.none()
            cart_item_ids = set(cart_items.values_list('menu_item_id', flat=True))
        else:
            cart_items = CartItem.objects.none()  # Empty QuerySet if no cart_id in session
            cart_item_ids = set()

    categories = Menu.objects.values('category').distinct()  # Get distinct categories
    menu_items = Menu.objects.all()  # Get all menu items
    return render(request, 'menu.html', {
        'menu_items': menu_items,
        'categories': categories,
        'cart_items': cart_items,  # Pass the cart items to the template
        'cart_item_ids': cart_item_ids,  # Pass the set of item ids that are in the cart
    })

@superuser_or_multiple_groups_required(['manager', 'Admin'])
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

@superuser_or_multiple_groups_required(['manager', 'Admin'])
def user_list_view(request):
    """Retrieve all users and render to an HTML template."""
    if request.user.is_authenticated:  # Ensure the user is logged in
        users = User.objects.all()  # Retrieve all users
        return render(request, 'user_list.html', {'users': users})
    else:
        return render(request, 'login.html', {'error': 'You must be logged in to view this page.'})

@superuser_or_multiple_groups_required(['manager', 'Admin'])
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

def delete_menu_item(request, item_id):
    if request.method == 'POST':
        menu_item = get_object_or_404(Menu, id=item_id)
        menu_item.delete()  # Delete the item from the database
        return redirect('menu')  # Redirect to the menu page with a success message
    
#Group creation
@login_required
@superuser_or_multiple_groups_required(['manager', 'Admin'])
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

@superuser_or_multiple_groups_required(['manager', 'Admin'])
def remove_user_from_group(request, group_id, user_id):
    group = Group.objects.get(id=group_id)
    user = User.objects.get(id=user_id)
    group.user_set.remove(user)
    return redirect('group_detail', group_id=group.id)

@superuser_or_multiple_groups_required(['manager', 'Admin'])
def remove_permission_from_group(request, group_id, perm_id):
    group = Group.objects.get(id=group_id)
    permission = Permission.objects.get(id=perm_id)
    group.permissions.remove(permission)
    return redirect('group_detail', group_id=group.id)


# Groups
# --------------

# Check if user is admin
@superuser_or_multiple_groups_required(['manager', 'Admin'])
def manage_groups(request):
    groups = Group.objects.all()
    return render(request, 'manage_groups.html', {'groups': groups})

# Add new Group with permissions
@superuser_or_multiple_groups_required(['manager', 'Admin'])
def add_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('name')
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            permissions = request.POST.getlist('permissions')
            group.permissions.set(Permission.objects.filter(id__in=permissions))
        return redirect('manage_groups')
    permissions = Permission.objects.all()
    return render(request, 'add_group.html', {'permissions': permissions})

# Details of Each Group
@superuser_or_multiple_groups_required(['manager', 'Admin'])
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    users = User.objects.exclude(groups=group)  # Users not in this group
    permissions = Permission.objects.all()

    if request.method == 'POST':
        if 'add_user' in request.POST:
            user_id = request.POST.get('user_id')
            user = User.objects.get(id=user_id)
            group.user_set.add(user)
        elif 'remove_user' in request.POST:
            user_id = request.POST.get('user_id')
            user = User.objects.get(id=user_id)
            group.user_set.remove(user)
        elif 'add_permission' in request.POST:
            perm_id = request.POST.get('perm_id')
            permission = Permission.objects.get(id=perm_id)
            group.permissions.add(permission)
        elif 'remove_permission' in request.POST:
            perm_id = request.POST.get('perm_id')
            permission = Permission.objects.get(id=perm_id)
            group.permissions.remove(permission)

        # Redirect to the same page after updating
        return redirect('group_detail', group_id=group.id)

    return render(request, 'group_detail.html', {
        'group': group,
        'users': users,
        'permissions': permissions,
    })


#Deliver Crew Features
@login_required
@superuser_or_multiple_groups_required(['manager', 'Admin', 'Delivery Crew'])
def delivery_crew_dashboard(request):
    # Show orders assigned to the logged-in delivery crew member
    orders = Order.objects.filter(delivery_crew=request.user, status=False)
    return render(request, 'delivery_dashboard.html', {'orders': orders})

@login_required
def update_order_status(request, order_id):
    # Get the order based on the provided order_id
    order = get_object_or_404(Order, id=order_id, delivery_crew=request.user)

    # Check if the order has already been delivered
    if order.status:
        return redirect('delivery_crew_dashboard')  # Redirect if the order is already delivered

    if request.method == 'POST':
        # Update order status to delivered
        order.status = True
        order.save()
        return redirect('delivery_crew_dashboard')  # Redirect to dashboard after updating status

    return render(request, 'update_order_status.html', {'order': order})

@login_required
def place_order(request):
    # Ensure the user has items in the cart
    cart = Cart.objects.get(user=request.user)
    if not cart.items.exists():
        return redirect('cart_detail')  # If the cart is empty, redirect to the cart page

    # Create a new order for the user
    total_cost = sum(item.total_price for item in cart.items.all())  # Calculate total price of items in cart
    order = Order.objects.create(
        user=request.user,
        total=total_cost,
        status=False,  # Initially, status is False (pending)
        date=datetime.date.today(),
    )

    # Add items to the order
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            menuitem=item.menu_item,
            quantity=item.quantity,
            price=item.total_price,
        )

    # Delete the cart items after placing the order
    cart.items.all().delete()  # Ensure the items are properly deleted or dissociated

    # Redirect to a confirmation or order details page
    return redirect('order_confirmation', order_id=order.id)


@login_required
def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'order_confirmation.html', {'order': order})

@login_required
def order_history(request):
    # Get all orders for the logged-in user
    orders = Order.objects.filter(user=request.user).order_by('-date')  # Ordered by most recent

    return render(request, 'order_history.html', {'orders': orders})


@login_required
@login_required
def assign_delivery_crew(request, order_id):
    # Get the order
    order = get_object_or_404(Order, id=order_id)

    # Check if the order is still pending and no crew assigned
    if order.status or order.delivery_crew:
        return HttpResponse("Order already completed or delivery crew assigned", status=400)

    # Handle POST request
    if request.method == 'POST':
        delivery_crew_id = request.POST.get('delivery_crew')
        if delivery_crew_id:
            delivery_crew = get_object_or_404(User, id=delivery_crew_id)

            # Assign the delivery crew to the order
            order.delivery_crew = delivery_crew
            order.save()

            # Redirect to the orders list or confirmation page
            return redirect('orders_list')

    # For GET requests, show the form
    delivery_crew = User.objects.filter(groups__name='Delivery Crew')
    return render(request, 'assign_delivery_crew.html', {'order': order, 'delivery_crew': delivery_crew})



def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # Get all delivery crew members (users with 'delivery crew' group)
    delivery_crew = User.objects.filter(groups__name='delivery crew')
    return render(request, 'order_detail.html', {'order': order, 'delivery_crew': delivery_crew})

def orders_list(request):
    orders = Order.objects.all()
    delivery_crew = User.objects.filter(groups__name='Delivery Crew')  # Get delivery crew members
    return render(request, 'orders_list.html', {'orders': orders, 'delivery_crew': delivery_crew})