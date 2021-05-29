"""mac URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static

# import users
from . import views
from users import views as user_views
from django.contrib.auth import views as auth_views  #django inbuilt library for creating login page.


urlpatterns = [
    path('admin/', admin.site.urls), 
    path('shop/',include('shop.urls')),
    path('blog/',include('blog.urls')),
    path('',views.index),
    path('profile/',user_views.profile,name='profile'),
    path('register/',user_views.register,name='register'), # Alternate way to go to register
    # path('register/',include('users.urls'))

    # if we didn't entered template_name then it would take a default location of login.html which is registration/login.html so for that we have to create a registration folder and then login.html....
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)