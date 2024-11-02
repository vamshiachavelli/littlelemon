from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path('menu/', views.MenuItemsView.as_view(), name='menu-items'),
    path('menu/<int:pk>/', views.menu_item_detail, name='menu_item_detail'),
    path('message/', views.msg),
    path('api-token-auth/', obtain_auth_token),
    path('index', views.index, name='index'),
    path('home', views.home, name='home'),
    path('about', views.about, name='about'),
    path('menu', views.menu, name='menu'),
    path('booking', views.booking, name='booking'),
    path('add-menu-item/', views.add_menu_item, name='add_menu_item'),
    path('book/', views.book_table, name='book_table'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
