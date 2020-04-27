

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('watch-now', views.watch_now, name='watch_now'),
    path('search', views.search, name='search'),
    path('search_a', views.search_a, name='search_a'),
    path('catalog/<slug>', views.category, name='category'),
    path('catalog/<slug>/<subcat_slug>', views.subcategory, name='subcategory'),
    path('video/<video_slug>', views.video_page, name='video_page'),
    path('recomended', views.recomended, name='recomended'),
    path('trends', views.trends, name='trends'),
    path('podcasts', views.podcasts, name='podcasts'),



]
