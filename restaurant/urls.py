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
    path('users/', views.UserListView.as_view(), name='user-list-api'),  # Ensure this matches
    path('api/menu/', views.MenuItemsView.as_view(), name='menu-items'),  # Example for API endpoint
    path('api/menu/<int:pk>/', views.SingleMenuItemView.as_view(), name='single-menu-item'),  # URL for single menu item
    path('api/SingleMenuItemView/', views.SingleMenuItemView.as_view(), name='SingleMenuItemView'),
    path('api-token-auth/', obtain_auth_token),
    path('all-users/', views.user_list_view, name='user_list'),  # Add this line
    path('registration_success/<int:user_id>/', views.registration_success, name='registration_success'),  # Updated URL
    path('dish-of-the-day/', views.dish_of_the_day, name='dish_of_the_day'),
    path('toggle-dish-of-the-day/<int:item_id>/', views.toggle_dish_of_the_day, name='toggle_dish_of_the_day'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('menu/delete/<int:item_id>/', views.delete_menu_item, name='delete_menu_item'),
    path('groups/', views.manage_groups, name='manage_groups'),
    path('groups/add/', views.add_group, name='add_group'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    path('remove_permission/<int:group_id>/<int:perm_id>/', views.remove_permission_from_group, name='remove_permission_from_group'),
    path('remove_user/<int:group_id>/<int:user_id>/', views.remove_user_from_group, name='remove_user_from_group'),
    path('delivery-dashboard/', views.delivery_crew_dashboard, name='delivery_crew_dashboard'),
    path('update-order-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('order-history/', views.order_history, name='order_history'),
    path('assign-delivery-crew/<int:order_id>/', views.assign_delivery_crew, name='assign_delivery_crew'),
    path('order-detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/', views.orders_list, name='orders_list'),
    path('manager-dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('home-clear-manager/', views.home_clear_manager, name='home_clear_manager'),
    path('delivery-crew-list/', views.delivery_crew_list, name='delivery_crew_list'),
    path('remove-delivery-crew/<int:user_id>/', views.remove_delivery_crew, name='remove_delivery_crew'),
    path('delete_user/<int:user_id>/', views.delete_user_view, name='delete_user'),
    path('edit_user/<int:user_id>/', views.edit_user_view, name='edit_user'),

    
    path('', include(router.urls)),

    # Add more patterns as needed
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
