from django.urls import path
from . import views

urlpatterns = [

   path('new/', views.new_video, name='new_video'),
   path('reaction_video/', views.reaction_video, name='reaction_video'),
   path('reaction_comment/', views.reaction_comment, name='reaction_comment'),

   path('add_comment_video/', views.add_comment_video, name='add_comment_video'),
   path('get_subcat/', views.get_subcat, name='get_subcat'),



]
