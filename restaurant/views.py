from rest_framework import generics, viewsets
from .models import Menu, Booking
from .serializers import MenuItemSerializer, BookingSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MenuForm,BookingForm

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

@api_view()
@permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
def msg(request):
    return Response({"message":"This view is protected"})

def index(request):
    return render(request,"index.html")

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def booking(request):
    return render(request, 'booking.html')

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
