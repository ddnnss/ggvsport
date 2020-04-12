from django.contrib import messages

from django.contrib.auth import login, logout,authenticate
from django.shortcuts import render, get_object_or_404
from .forms import SignUpForm,UpdateForm
from customuser.models import *
from django.http import JsonResponse, HttpResponseRedirect
from category.models import Category
import settings

def login_req(request):
    user = authenticate(username=request.POST.get('email'), password=request.POST.get('password'))
    if user is not None:
        login(request, user)
        return HttpResponseRedirect("/user/profile")
    else:
        messages.success(request, 'Проверьте введенные данные')
        return HttpResponseRedirect('/login')

def register(request):
    print(request.POST)
    data = request.POST.copy()

    form = SignUpForm(data)
    print(form.errors)
    if form.is_valid():
        new_user = form.save(data)
        login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect('/')
    else:
        form = SignUpForm()
    return HttpResponseRedirect("/")


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


def profile(request):
    if request.user.is_authenticated:
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
                    success = user.check_password(request.POST['old_password'])
                    if success:
                        print('Old pass is good')
                        if request.POST.get('password1') == request.POST.get('password2'):
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
