from django.http import HttpResponseRedirect
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