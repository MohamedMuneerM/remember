"""remember URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from accounts.views import register, Plans, profile, upgrade
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('upgrade/', upgrade, name='upgrade'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/',include('backend.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='frontend/pages/auth/login.html'), name='login'),
    path('plans/', Plans.as_view(), name='plans'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
