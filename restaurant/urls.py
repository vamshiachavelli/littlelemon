from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token


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
    path('login/', views.login_view, name='Login'),
    path('logout/', views.logout_view, name='Logout'),
    path('register/', views.register, name='register'),
    path('users/', views.UserListView.as_view(), name='user-list'),  # Ensure this matches
    path('api/menu/', views.MenuItemsView.as_view(), name='menu-items'),  # Example for API endpoint
    path('api/menu/<int:pk>/', views.SingleMenuItemView.as_view(), name='single-menu-item'),  # URL for single menu item
    path('api/SingleMenuItemView/', views.SingleMenuItemView.as_view(), name='SingleMenuItemView'),
    path('api-token-auth/', obtain_auth_token),
    path('use/', views.user_list_view, name='user_list'),  # Add this line
    path('registration_success/<int:user_id>/', views.registration_success, name='registration_success'),  # Updated URL
    path('dish-of-the-day/', views.dish_of_the_day, name='dish_of_the_day'),
    path('toggle-dish-of-the-day/<int:item_id>/', views.toggle_dish_of_the_day, name='toggle_dish_of_the_day'),
    path('', include(router.urls)),

    # Add more patterns as needed
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
