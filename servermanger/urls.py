from django.urls import path
from django.contrib.auth.views import login
from . import views

app_name='servermanger'

urlpatterns = [
    path('server_list', views.server_list, name='server_list'),
    path('server_edit/<int:item_id>/', views.server_edit, name='server_edit'),
    path('server_delete/<int:item_id>/', views.server_delete, name='server_delete'),
    path('server_add/', views.server_add, name='server_add'),
    path('server_search', views.server_search, name='server_search'),
]