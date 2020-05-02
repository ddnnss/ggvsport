from django.urls import path
from . import views

urlpatterns = [

   path('new/', views.new_video, name='new_video'),
   path('update/', views.update_video, name='update_video'),
   path('reaction_video/', views.reaction_video, name='reaction_video'),
   path('reaction_comment/', views.reaction_comment, name='reaction_comment'),
   path('delete/<video_id>', views.video_delete, name='video_delete_by_user'),
   path('delete_comment/', views.delete_comment, name='delete_comment'),

   path('add_comment_video/', views.add_comment_video, name='add_comment_video'),
   path('get_subcat/', views.get_subcat, name='get_subcat'),



]
