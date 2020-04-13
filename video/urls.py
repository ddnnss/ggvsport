from django.urls import path
from . import views

urlpatterns = [

   path('new/', views.new_video, name='new_video'),
   path('like_video/', views.like_video, name='like_video'),


]
