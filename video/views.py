import json

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
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
        if request.POST.get('subcategory'):
            video.subcategory_id = request.POST.get('subcategory')
        video.save()
        return HttpResponseRedirect('/user/profile/#tab-1')
    else:
        form = CreateVideo()
        return render(request, 'user/profile-add-video.html', locals())


def reaction_video(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    video = Video.objects.get(id=body['v_id'])
    user_id = body['r_from']
    print(video)
    video_is_like = False
    if body['r_type'] == 'like':
        print('like')
        video_is_like = True
    reaction = None
    try:
        reaction = VideoLike.objects.get(video=video,user_id=user_id)
        reaction.delete()
        print(reaction.is_like)
        print('Reaction found')
    except:
        print('Reaction NOT found')
        VideoLike.objects.create(video=video,user_id=user_id,is_like=video_is_like)







    return JsonResponse({'status':'ok'})
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
        comments.append({
            'avatar': c.user.get_avatar(),
            'nickname': c.user.get_nickname(),
            'likes': c.likes,
            'dislikes': c.dislikes,
            'comment': c.comment,
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