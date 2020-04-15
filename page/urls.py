

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('watch-now', views.watch_now, name='watch_now'),
    path('catalog/<slug>', views.category, name='category'),
    path('catalog/<slug>/<subcat_slug>', views.subcategory, name='subcategory'),
    path('video/<video_slug>', views.video_page, name='video_page'),




]
