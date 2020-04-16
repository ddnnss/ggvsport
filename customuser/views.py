import json

from django.contrib import messages

from django.contrib.auth import login, logout,authenticate
from django.shortcuts import render, get_object_or_404
from .forms import SignUpForm,UpdateForm
from customuser.models import *
from django.http import JsonResponse, HttpResponseRedirect
from category.models import Category
from video.models import *
from video.forms import *
import settings

def login_req(request):
    request_unicode = request.body.decode('utf-8')
    request_body = json.loads(request_unicode)
    print(request_body)
    user = authenticate(username=request_body['email'], password=request_body['password'])
    if user is not None:
        login(request, user)
        return JsonResponse({'status': 'success'}, safe=False)
    else:
        return JsonResponse({'status':'error'}, safe=False)

def register(request):
    print(request.POST)
    request_unicode = request.body.decode('utf-8')
    request_body = json.loads(request_unicode)
    data = request.POST.copy()

    form = SignUpForm(request_body)
    print(form.errors)
    if form.is_valid():
        new_user = form.save(data)
        new_user.is_social_reg = False
        new_user.save()
        login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
        return JsonResponse({'status': 'success'}, safe=False)
    else:

        return JsonResponse({'status':'error','errors': form.errors}, safe=False)


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


def profile(request):
    if request.user.is_authenticated:
        own_videos = Video.objects.filter(user=request.user)
        try:
            fav_videos = FavoriteVideo.objects.get(user=request.user)
        except:
            fav_videos = FavoriteVideo.objects.create(user=request.user)
        return render(request, 'user/profile.html', locals())
    else:
        return HttpResponseRedirect('/')


def profile_edit(request):
    if request.user.is_authenticated:
        if request.POST:
            print(request.POST)

            form = UpdateForm(request.POST, request.FILES, instance=request.user)
            print(form.errors)
            if form.is_valid():
                user = form.save()
                if request.POST.get('ismale'):
                    user.genre = True
                if request.POST.get('isfemale'):
                    user.genre = False
                if request.POST.get('fav_cat1') != '0':
                    user.fav_category1_id = int(request.POST.get('fav_cat1'))
                else:
                    user.fav_category1 = None
                if request.POST.get('fav_cat2') != '0':
                    user.fav_category2_id = int(request.POST.get('fav_cat2'))
                else:
                    user.fav_category2 = None
                if request.POST.get('fav_cat3') != '0':
                    user.fav_category3_id = int(request.POST.get('fav_cat3'))
                else:
                    user.fav_category3 = None
                if request.POST.get('fav_cat4') != '0':
                    user.fav_category4_id = int(request.POST.get('fav_cat4'))
                else:
                    user.fav_category4 = None

                if request.POST.get('old_password'):
                    if not user.is_social_reg:
                        success = user.check_password(request.POST['old_password'])
                    else:
                        success = True
                    if success:
                        print('Old pass is good')
                        if request.POST.get('password1') == request.POST.get('password2') and request.POST.get('password1') != '' and request.POST.get('password2') != '':
                            print('Change password')
                            user.set_password(request.POST.get('password1'))
                        else:
                            print('NOT Change password')
                    else:
                        print('Old pass is bad')
                        return HttpResponseRedirect("/user/profile/edit")
                user.save()
                return HttpResponseRedirect('/user/profile/edit')
            else:
                form = UpdateForm()
            return HttpResponseRedirect("/user/profile/edit")
        dates = ['01', '02', '03', '04']
        months = ['Январь', 'Февраль']
        years = ['1950', '1951']
        allCats = Category.objects.all()
        updateForm = UpdateForm()
        return render(request, 'user/profile-edit.html', locals())
    else:
        return HttpResponseRedirect('/')

def profile_add(request):
    if request.user.is_authenticated:
        form = CreateVideo()
        return render(request, 'user/profile-add-video.html', locals())
    else:
        return HttpResponseRedirect('/')

def profile_history(request):
    if request.user.is_authenticated:
        try:
            history_videos = VideoHistory.objects.get(user=request.user)
        except:
            history_videos = None
        return render(request, 'user/profile-history.html', locals())
    else:
        return HttpResponseRedirect('/')