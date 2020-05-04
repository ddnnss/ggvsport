import json

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from .forms import *
from .models import *
def new_video(request):
    print(request.POST)
    form = CreateVideo(request.POST, request.FILES)
    print(form.errors)
    if form.is_valid():
        video = form.save(commit=False)
        video.user = request.user
        video.category_id = request.POST.get('category')
        if request.POST.get('subcategory') != '0':
            video.subcategory_id = request.POST.get('subcategory')
        video.save()
        return HttpResponseRedirect('/user/profile/#tab-1')
    else:
        form = CreateVideo()
        return render(request, 'user/profile-add-video.html', locals())

def update_video(request):
    print(request.POST)
    video = get_object_or_404(Video, id=request.POST.get('video_id'))
    if video.user == request.user or request.user.is_superuser:
        form = EditVideo(request.POST, request.FILES, instance=video)
        print(form.errors)
        if form.is_valid():
            video = form.save(commit=False)
            video.category_id = request.POST.get('category')
            if request.POST.get('subcategory') != '0':
                video.subcategory_id = request.POST.get('subcategory')
            video.save()
            return HttpResponseRedirect(f'/{request.LANGUAGE_CODE}/video/{video.name_slug}')
        else:
            form = EditVideo()
            return render(request, 'user/profile-add-video.html', locals())
def reaction_video(request):
    if request.user.is_authenticated:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        video = Video.objects.get(id=body['v_id'])
        user_id = str(body['r_from'])
        print(video)
        video_is_like = False
        all_likes = video.liked_by_users.split(',')
        all_dislikes = video.disliked_by_users.split(',')
        try:
            fav = FavoriteVideo.objects.get(user_id=user_id)
        except:
            fav = FavoriteVideo.objects.create(user_id=user_id)
        if body['r_type'] == 'like':
            print('like')
            video_is_like = True

        if video_is_like:
            print('all_likes',all_likes)
            if not user_id in all_likes:
                all_likes.append(user_id)
                video.likes +=1
                fav.videos.add(video)
                print('set like')
                if user_id in all_dislikes:
                    all_dislikes.remove(user_id)
                    video.dislikes -= 1
                    print('retset dislike')
                    video.disliked_by_users = ','.join(all_dislikes)
                video.liked_by_users = ','.join(all_likes)
            else:
                all_likes.remove(user_id)
                video.likes -= 1
                print('retset like')
                fav.videos.remove(video)
                video.liked_by_users = ','.join(all_likes)


        else:
            print('all_dislikes', all_dislikes)
            if not user_id in all_dislikes:
                all_dislikes.append(user_id)
                video.dislikes += 1
                fav.videos.remove(video)
                print('set dislike')
                if user_id in all_likes:
                    all_likes.remove(user_id)
                    video.likes -= 1
                    print('retset like')
                    video.liked_by_users = ','.join(all_likes)
                video.disliked_by_users = ','.join(all_dislikes)
            else:
                all_dislikes.remove(user_id)
                video.dislikes -= 1
                print('retset dislike')
                video.disliked_by_users = ','.join(all_dislikes)
        video.save()
        return JsonResponse({'likes':video.likes,'dislikes':video.dislikes})
    else:
        return JsonResponse({'status': 'not auth'})

def reaction_comment(request):
    if request.user.is_authenticated:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        comment = CommentVideo.objects.get(id=body['c_id'])
        user_id = str(body['r_from'])
        print(comment)
        video_is_like = False
        all_likes = comment.liked_by_users.split(',')
        all_dislikes = comment.disliked_by_users.split(',')
        if body['r_type'] == 'like':
            print('like')
            video_is_like = True

        if video_is_like:
            print('all_likes',all_likes)
            if not user_id in all_likes:
                all_likes.append(user_id)
                comment.likes +=1
                print('set like')
                if user_id in all_dislikes:
                    all_dislikes.remove(user_id)
                    comment.dislikes -= 1
                    print('retset dislike')
                    comment.disliked_by_users = ','.join(all_dislikes)
                comment.liked_by_users = ','.join(all_likes)
            else:
                all_likes.remove(user_id)
                comment.likes -= 1
                print('retset like')
                comment.liked_by_users = ','.join(all_likes)


        else:
            print('all_dislikes', all_dislikes)
            if not user_id in all_dislikes:
                all_dislikes.append(user_id)
                comment.dislikes += 1
                print('set dislike')
                if user_id in all_likes:
                    all_likes.remove(user_id)
                    comment.likes -= 1
                    print('retset like')
                    comment.liked_by_users = ','.join(all_likes)
                comment.disliked_by_users = ','.join(all_dislikes)
            else:
                all_dislikes.remove(user_id)
                comment.dislikes -= 1
                print('retset dislike')
                comment.disliked_by_users = ','.join(all_dislikes)
        comment.save()
        return JsonResponse({'likes':comment.likes,'dislikes':comment.dislikes})
    else:
        return JsonResponse({'status': 'not auth'})

def add_comment_video(request):
    return_dict = {}
    comments = []
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    print(body)
    comment = CommentVideo.objects.create(user_id=body['c_from'], video_id=body['v_id'], comment=body['c_text'])
    comment.video.comments += 1
    comment.video.save()
    for c in comment.video.commentvideo_set.all().order_by('-created_at'):
        is_liked = ''
        is_disliked = ''
        all_likes = c.liked_by_users.split(',')
        all_dislikes = c.disliked_by_users.split(',')
        if str(request.user.id) in all_likes:
            is_liked = 'active'
        if str(request.user.id) in all_dislikes:
            is_disliked = 'active'
        comments.append({
            'id': c.id,
            'admin':request.user.is_superuser,
            'u_id':c.user.id,
            'avatar': c.user.get_avatar(),
            'nickname': c.user.get_nickname(),
            'likes': c.likes,
            'dislikes': c.dislikes,
            'comment': c.comment,
            'liked': is_liked,
            'disliked': is_disliked,
            'dt': c.get_created_time()
        })
    return_dict['comments'] = comments
    print(return_dict)
    return JsonResponse(return_dict)

def get_subcat(request):
    body = json.loads(request.body)
    return_dict = {}
    print(body)
    return_dict['subcategories'] = list()
    subcategories = SubCategory.objects.filter(category=body['category'])
    for subcat in subcategories:
         return_dict['subcategories'].append({'id':subcat.id,
                                              'name': subcat.name})
    return JsonResponse(return_dict)


def video_delete(request,video_id):
    video = get_object_or_404(Video, id=video_id)
    if video.user == request.user or request.user.is_superuser:
        video.delete()
        return HttpResponseRedirect('/user/profile/#tab-1')
    else:
        return HttpResponseRedirect('/')


def delete_comment(request):
    return_dict = {}
    comments = []
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    print(body)
    comment = CommentVideo.objects.get(id=body['c_id'])
    comment.delete()
    for c in comment.video.commentvideo_set.all().order_by('-created_at'):
        is_liked = ''
        is_disliked = ''
        all_likes = c.liked_by_users.split(',')
        all_dislikes = c.disliked_by_users.split(',')
        if str(request.user.id) in all_likes:
            is_liked = 'active'
        if str(request.user.id) in all_dislikes:
            is_disliked = 'active'
        comments.append({
            'id': c.id,
            'admin': request.user.is_superuser,
            'u_id': c.user.id,
            'avatar': c.user.get_avatar(),
            'nickname': c.user.get_nickname(),
            'likes': c.likes,
            'dislikes': c.dislikes,
            'comment': c.comment,
            'liked': is_liked,
            'disliked': is_disliked,
            'dt': c.get_created_time()
        })
    return_dict['comments'] = comments
    print(return_dict)
    return JsonResponse(return_dict)
