from django.urls import path
from . import views

urlpatterns = [

   path('new/', views.new_video, name='new_video'),
   path('like_video/', views.like_video, name='like_video'),
   path('dislike_video/', views.dislike_video, name='dislike_video'),
   path('add_comment_video/', views.add_comment_video, name='add_comment_video'),



]
