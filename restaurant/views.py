from rest_framework import generics
from .models import MenuItem
from .serializers import MenuItemSerializer

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):  # Use this to combine Retrieve, Update, and Destroy
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
