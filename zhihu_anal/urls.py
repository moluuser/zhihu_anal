"""zhihu_anal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from dashboard import views
import captcha

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('statement/', views.statement, name='statement'),
    path('register/', views.register, name='register'),
    path('zhihuuser/', views.zhihuuser, name='zhihuuser'),
    path('logout/', views.logout, name='logout'),
    path('users/', views.users, name='users'),
    path('captcha/', include('captcha.urls')),
    path('delete/', views.delete, name='delete'),
    path('edit/', views.edit, name='edit'),
    path('useranal/', views.useranal, name='useranal'),
    path('contentanal/', views.contentanal, name='contentanal'),
    path('zhihuque/', views.zhihuque, name='zhihuque'),
    path('search/', views.search, name='search'),
    path('zhihutag/', views.zhihutag, name='zhihutag'),
]
