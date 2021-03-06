import json

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from category.models import *
from .models import *
from video.models import *
import datetime as dt
from datetime import datetime
from django.utils import timezone
from itertools import chain
from django.db.models import Q

def index(request):
    index_page = True
    try:
        tags = SeoTag.objects.first()
        h1 = tags.index_h1
        title = tags.index_title
        description = tags.index_description
    except:
        pass
    h1 = 'H1'
    watch_now_videos = Video.objects.filter(is_now_watching=True, is_moderated=True)
    for v in watch_now_videos:

        if (timezone.now() - v.start_watch) > dt.timedelta(seconds=v.duration):
            v.is_now_watching = False
            v.save()
    if watch_now_videos:
        try:
            top2_watch_now_videos = watch_now_videos.order_by('-likes')[:2]
            other_watch_now_videos = watch_now_videos.exclude(id__in=top2_watch_now_videos)
        except:
            other_watch_now_videos = watch_now_videos

    podcats_videos = Video.objects.filter(category__is_podcast=True, is_moderated=True)

    if podcats_videos:
        try:
            top2_podcats_videos = podcats_videos.order_by('-likes')[:2]
            other_podcats_videos = podcats_videos.exclude(id__in=top2_podcats_videos)[:4]
        except:
            other_podcats_videos = podcats_videos

    if request.user.is_authenticated:
        user=request.user
        fav_videos1 = []
        fav_videos2 = []
        fav_videos3 = []
        fav_videos4 = []
        if user.fav_category1:
            fav_videos1 = Video.objects.filter(category=user.fav_category1).order_by('-likes')
        if user.fav_category2:
            fav_videos2 = Video.objects.filter(category=user.fav_category2).order_by('-likes')
        if user.fav_category3:
            fav_videos3 = Video.objects.filter(category=user.fav_category3).order_by('-likes')
        if user.fav_category4:
            fav_videos4 = Video.objects.filter(category=user.fav_category4).order_by('-likes')
        all_recomended_videos = list(chain(fav_videos1, fav_videos2, fav_videos3, fav_videos4))
        if all_recomended_videos:
            try:
                top3_all_recomended_videos = all_recomended_videos[:3]
                other_all_recomended_videos = set(all_recomended_videos) - set(top3_all_recomended_videos)[:4]
                print(other_all_recomended_videos)
            except:
                other_all_recomended_videos = all_recomended_videos

    return render(request, 'page/index.html', locals())

def category(request,slug):
    category = get_object_or_404(Category, name_slug=slug)
    title = category.page_title
    description = category.page_description
    tle = category.page_keywords
    h1 = category.page_h1

    all_videos = Video.objects.filter(category=category,is_moderated=True)
    try:
        top2_video = all_videos.order_by('-likes')[:2]
        top5_video = all_videos.order_by('-likes')[3:6]
        other_videos = all_videos.exclude(id__in=top2_video).exclude(id__in=top5_video)
    except:
        other_videos = all_videos
    return render(request, 'page/category.html', locals())

def subcategory(request,slug,subcat_slug):
    subcategory = get_object_or_404(SubCategory, name_slug=subcat_slug)
    title = subcategory.page_title
    description = subcategory.page_description
    tle = subcategory.page_keywords
    h1 = subcategory.page_h1
    all_videos = Video.objects.filter(subcategory=subcategory,is_moderated=True)
    try:
        top2_video = all_videos.order_by('-likes')[:2]
        top5_video = all_videos.order_by('-likes')[3:6]
        other_videos = all_videos.exclude(id__in=top2_video).exclude(id__in=top5_video)
    except:
        other_videos = all_videos
    return render(request, 'page/subcategory.html', locals())

def watch_now(request):
    watch_now_videos = Video.objects.filter(is_now_watching=True, is_moderated=True)
    for v in watch_now_videos:
        if (timezone.now() - v.start_watch) > dt.timedelta(seconds=v.duration):
            v.is_now_watching = False
            v.save()
    if watch_now_videos:
        try:
            top2_watch_now_videos = watch_now_videos.order_by('-likes')[:2]
            top5_watch_now_videos = watch_now_videos.order_by('-likes')[3:6]
            other_watch_now_videos = watch_now_videos.exclude(id__in=top2_watch_now_videos).exclude(id__in=top5_watch_now_videos)
        except:
            other_watch_now_videos = watch_now_videos

    return render(request, 'page/now-watch.html', locals())
def video_page(request,video_slug):
    video = get_object_or_404(Video, name_slug=video_slug)

    own_video = True
    all_comments = CommentVideo.objects.filter(video=video).order_by('-created_at')
    video.is_now_watching = True
    video.start_watch = datetime.now()
    watch_now_videos = Video.objects.filter(is_now_watching=True, is_moderated=True).exclude(id=video.id)
    is_liked = False
    is_disliked = False
    for v in watch_now_videos:
        if (timezone.now() - v.start_watch) > dt.timedelta(seconds=v.duration):
            v.is_now_watching = False
            v.save()
    if request.user.is_authenticated:
        all_likes = video.liked_by_users.split(',')
        all_dislikes = video.disliked_by_users.split(',')
        if str(request.user.id) in all_likes:
            is_liked = True
        if str(request.user.id) in all_dislikes:
            is_disliked = True
        try:
            history = VideoHistory.objects.get(user=request.user)
            history.video.add(video)
        except:
            history = VideoHistory.objects.create(user=request.user)
            history.video.add(video)
        history.save()
        if not request.user == video.user:
            video.views += 1
            own_video = False
    video.save()
    return render(request, 'page/video.html', locals())

def search(request):
    q = request.GET.get('query').lower()
    search_result = Video.objects.filter(Q(name_lower__contains=q) | Q(description__contains=q))
    search_result = search_result.filter(is_moderated=True)
    return render(request, 'page/search.html', locals())


def search_a(request):
    request_unicode = request.body.decode('utf-8')
    request_body = json.loads(request_unicode)
    print(request_body)
    search_result = Video.objects.filter(Q(name_lower__contains=request_body['query']) | Q(description__contains=request_body['query']))
    search_result = search_result.filter(is_moderated=True)
    return_dict = list()
    for i in search_result:
        try:
            return_dict.append({'url': i.get_absolute_url(), 'name': i.name})
        except:
            pass
    return JsonResponse(return_dict, safe=False)


def podcasts(request):
    try:
        tags = SeoTag.objects.first()

        title = tags.podcast_title
        description = tags.podcast_description
    except:
        pass

    all_videos = Video.objects.filter(category__is_podcast=True, is_moderated=True)
    try:
        top2_video = all_videos.order_by('-likes')[:2]
        top5_video = all_videos.order_by('-likes')[3:6]
        other_videos = all_videos.exclude(id__in=top2_video).exclude(id__in=top5_video)
    except:
        other_videos = all_videos

    return render(request, 'page/all_podcasts.html', locals())

def recomended(request):
    try:
        tags = SeoTag.objects.first()

        title = tags.recomended_title
        description = tags.recomended_description
    except:
        pass
    user = request.user
    fav_videos1 = []
    fav_videos2 = []
    fav_videos3 = []
    fav_videos4 = []
    if user.fav_category1:
        fav_videos1 = Video.objects.filter(category=user.fav_category1).order_by('-likes')
    if user.fav_category2:
        fav_videos2 = Video.objects.filter(category=user.fav_category2).order_by('-likes')
    if user.fav_category3:
        fav_videos3 = Video.objects.filter(category=user.fav_category3).order_by('-likes')
    if user.fav_category4:
        fav_videos4 = Video.objects.filter(category=user.fav_category4).order_by('-likes')
    all_recomended_videos = list(chain(fav_videos1, fav_videos2, fav_videos3, fav_videos4))
    if all_recomended_videos:
        try:
            top3_all_recomended_videos = all_recomended_videos[:3]
            other_all_recomended_videos = set(all_recomended_videos) - set(top3_all_recomended_videos)
            print(other_all_recomended_videos)
        except:
            other_all_recomended_videos = all_recomended_videos
    return render(request, 'page/all_recomended.html', locals())

def trends(request):
    all_videos = Video.objects.all().order_by('likes')
    try:
        top2_video = all_videos.order_by('-likes')[:2]
        top5_video = all_videos.order_by('-likes')[3:6]
        other_videos = all_videos.exclude(id__in=top2_video).exclude(id__in=top5_video)
    except:
        other_videos = all_videos
    try:
        tags = SeoTag.objects.first()
        title = tags.trends_title
        description = tags.trends_description
    except:
        pass
    return render(request, 'page/trends.html', locals())