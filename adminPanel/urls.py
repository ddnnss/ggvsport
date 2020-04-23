from django.urls import path
from . import views

urlpatterns = [

   path('', views.admin_index, name='admin_index'),
   path('user/info/edit', views.admin_profile_edit, name='admin_profile_edit'),
   path('user/<user_id>', views.admin_user_info, name='admin_user_info'),

   path('category/create_cat', views.admin_create_category, name='admin_create_category'),
   path('category/update_cat', views.admin_update_category, name='admin_update_category'),
   path('category/create_subcat', views.admin_create_subcategory, name='admin_create_subcategory'),
   path('category/update_subcat', views.admin_update_subcategory, name='admin_update_subcategory'),
   path('category/delete_cat/<id>', views.delete_cat, name='admin_delete_cat'),
   path('category/delete_subcat/<id>', views.delete_subcat, name='admin_delete_subcat'),
   path('category/get_cat_info', views.get_cat_info, name='get_cat_info'),
   path('category/get_subcat_info', views.get_subcat_info, name='get_subcat_info'),
   path('video/delete/<id>', views.delete_video, name='delete_video'),
   path('video/moderate/<id>', views.moderate_video, name='moderate_video'),




]
