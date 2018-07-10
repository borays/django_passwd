from django.urls import path
from . import views

app_name='pwdmanger'

urlpatterns = [
    path('', views.passwd_list, name='passwd_list'),
    path('passwd_edit/<int:item_id>/', views.passwd_edit, name='passwd_edit'),
    path('passwd_delete/<int:item_id>/', views.passwd_delete, name='passwd_delete'),
    path('passwd_add/', views.passwd_add, name='passwd_add'),
]
