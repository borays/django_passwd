from django.urls import path
from . import views

app_name='pwdmanger'

urlpatterns = [
    path('passwd_list', views.passwd_list, name='passwd_list'),
    path('', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('passwd_edit/<int:item_id>/', views.passwd_edit, name='passwd_edit'),
    path('passwd_delete/<int:item_id>/', views.passwd_delete, name='passwd_delete'),
    path('passwd_add/', views.passwd_add, name='passwd_add'),
    path('api/update', views.api_update_pass, name='api_update_pass'),
    path('passwd_search', views.passwd_search, name='passwd_search'),
]
