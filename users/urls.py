from django.urls import path
from django.contrib.auth.views import login
from . import views

app_name='users'

urlpatterns = [
    path('user_login/', login, {'template_name': 'users/login.html'},name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('user_register/', views.user_register, name='user_register'),
    path('user_change_pass/', views.user_change_pass, name='user_change_pass'),
]