"""
URL configuration for littlelemon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token



urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("restaurant.urls")),  # Include your app URLs
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    #path('api-token-auth/', obtain_auth_token),
    #path('api/', include(router.urls)),  # Include router URLs
    #path('api/menu/', views.MenuItemsView.as_view(), name='menu_items'),  # API for menu items
    #path('api/menu/<int:pk>/', views.SingleMenuItemView.as_view(), name='single_menu_item'),
]