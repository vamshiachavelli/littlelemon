from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

# Set up the router for the Booking ViewSet
router = DefaultRouter()
router.register(r'bookings', views.BookingViewSet, basename='booking')


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('menu/', views.menu, name='menu'),
    path('menu/add/', views.add_menu_item, name='add_menu_item'),
    path('menu/<int:pk>/', views.menu_item_detail, name='menu_item_detail'),
    path('booking/', views.book_table, name='book_table'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('users/', views.UserListView.as_view(), name='user-list'),  # Ensure this matches
    path('api/menu/', views.MenuItemsView.as_view(), name='menu-items'),  # Example for API endpoint
    # Add more patterns as needed
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)