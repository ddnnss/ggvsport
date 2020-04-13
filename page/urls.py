

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<slug>', views.category, name='category'),
    path('category/<slug>/<subcat_slug>', views.subcategory, name='subcategory'),
    path('category/<slug>/<subcat_slug>/<video_slug>', views.video_page, name='video_page'),




]
