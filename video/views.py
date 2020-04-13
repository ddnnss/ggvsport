import json

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .forms import *
from .models import *
def new_video(request):
    form = CreateVideo(request.POST, request.FILES)
    print(form.errors)
    if form.is_valid():
        video = form.save(commit=False)
        video.user = request.user
        video.save()
    return HttpResponseRedirect('/user/profile/#tab-1')

def like_video(request):
    pass
def dislike_video(request):
    pass
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
