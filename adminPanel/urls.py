from django.urls import path
from . import views

urlpatterns = [

   path('', views.admin_index, name='admin_index'),
   path('user/<user_id>', views.admin_user_info, name='admin_user_info'),
   path('user/edit', views.admin_profile_edit, name='admin_profile_edit'),
   path('category/create', views.admin_create_category, name='admin_create_category'),


]
