import json

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from customuser.models import User
from customuser.forms import UpdateForm
from category.models import *
from category.forms import *
from video.models import *

def admin_index(request):
    if request.user.is_superuser:
        all_users = User.objects.filter(is_superuser=False)
        all_cats = Category.objects.all()
        all_moderated_video = Video.objects.filter(is_moderated=True)
        all_non_moderated_video = Video.objects.filter(is_moderated=False)
        newCategoryForm = NewCategory()
        newSubCategoryForm = NewSubCategory()
        return render(request, 'adminPanel/admin.html', locals())
    else:
        return HttpResponseRedirect('/')

def admin_user_info(request,user_id):
    if request.user.is_superuser:

        user = User.objects.get(id=user_id)
        updateForm = UpdateForm()
        allCats = Category.objects.all()
        dates = ['01', '02', '03', '04']
        months = ['Январь', 'Февраль']
        years = ['1950', '1951']
        return render(request, 'adminPanel/user-info.html', locals())
    else:
        return HttpResponseRedirect('/')

def admin_profile_edit(request):

    if request.POST:
        print(request.POST)
        user = User.objects.get(id=int(request.POST.get('id')))
        print(request.POST.get('block_user'))
        if request.POST.get('block_user'):
            print('disable user')
            user.is_active = False
            user.save()
            return HttpResponseRedirect('/cp')
        else:
            user.is_active = True
            user.save()
        form = UpdateForm(request.POST, request.FILES, instance=user)
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



            if request.POST.get('password1') == request.POST.get('password2') and request.POST.get('password1') != '' and request.POST.get('password2') != '':
                print('Change password')
                user.set_password(request.POST.get('password1'))
            else:
                print('NOT Change password')
            user.save()
            return HttpResponseRedirect('/cp')
        else:
            form = UpdateForm()
        return HttpResponseRedirect("/cp")

def admin_create_category(request):
    print(request.POST)
    if request.POST:

        form = NewCategory(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/cp/#tab-2')

def admin_update_category(request):
    print(request.POST)
    if request.POST:
        cat = Category.objects.get(id=request.POST.get('id'))
        form = NewCategory(request.POST, request.FILES,instance=cat)
        print(form.errors)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/cp/#tab-2')

def admin_create_subcategory(request):
    print(request.POST)
    if request.POST:
        form = NewSubCategory(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/cp/#tab-2')

def admin_update_subcategory(request):
    print(request.POST)
    if request.POST:
        cat = SubCategory.objects.get(id=request.POST.get('id'))
        form = UpdateSubCategory(request.POST, request.FILES,instance=cat)
        print(form.errors)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/cp/#tab-2')


def delete_cat(request,id):
    Category.objects.get(id=id).delete()
    return HttpResponseRedirect('/cp/#tab-2')

def delete_subcat(request,id):
    SubCategory.objects.get(id=id).delete()
    return HttpResponseRedirect('/cp/#tab-2')

def get_cat_info(request):
    body = json.loads(request.body)
    cat = Category.objects.get(id=body['id'])
    cat_info={
        'id': cat.id,
        'name': cat.name,
        'image': cat.image.url,
        'page_title': cat.page_title,
        'page_description': cat.page_description,
        'page_keywords': cat.page_keywords,
        'seo_text': cat.seo_text
    }
    return JsonResponse(cat_info)


def get_subcat_info(request):
    body = json.loads(request.body)
    cat = SubCategory.objects.get(id=body['id'])
    cat_info={
        'id': cat.id,
        'name': cat.name,
        'image': cat.image.url,
        'page_title': cat.page_title,
        'page_description': cat.page_description,
        'page_keywords': cat.page_keywords,
        'seo_text': cat.seo_text
    }
    return JsonResponse(cat_info)

def delete_video(request,id):
    Video.objects.get(id=id).delete()
    return HttpResponseRedirect(f'/cp/#t{request.GET.get("tab")}')

def moderate_video(request,id):
    video = Video.objects.get(id=id)
    video.is_moderated = True
    video.save()
    return HttpResponseRedirect('/cp/#tab-4')
