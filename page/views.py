from django.shortcuts import render, get_object_or_404
from category.models import *
from video.models import *

def index(request):
    return render(request, 'page/index.html', locals())

def category(request,slug):
    category = get_object_or_404(Category, name_slug=slug)
    return render(request, 'page/category.html', locals())

def subcategory(request,slug,subcat_slug):
    subcategory = get_object_or_404(SubCategory, name_slug=subcat_slug)
    all_videos = Video.objects.filter(subcategory=subcategory)
    try:
        top2_video = all_videos.order_by('-likes')[:2]
        top5_video = all_videos.order_by('-likes')[3:6]
        other_videos = all_videos.exclude(top2_video).exclude(top5_video)
    except:
        other_videos = all_videos
    return render(request, 'page/subcategory.html', locals())


def video_page(request,slug,subcat_slug,video_slug):
    video = get_object_or_404(Video, name_slug=video_slug)
    if not request.user == video.user:
        video.views +=1
        video.save()
    return render(request, 'page/video.html', locals())


