from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('login/', views.MyLogin.as_view(), name="login"),
    path('', views.account, name="account"),
    path('regenerate/', views.regenerate_table, name="regenerate"),
    path('withdrew/', views.withdrew, name='withdrew'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]
