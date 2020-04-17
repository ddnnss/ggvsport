from django.http import HttpResponseRedirect
from django.shortcuts import render
from customuser.models import User
from customuser.forms import UpdateForm
from category.models import *
from category.forms import *

def admin_index(request):
    if request.user.is_superuser:
        all_users = User.objects.filter(is_superuser=False)
        all_cats = Category.objects.all()
        newCategoryForm = NewCategory()
        return render(request, 'adminPanel/admin.html', locals())
    else:
        return HttpResponseRedirect('/')

def admin_user_info(request,user_id):
    if request.user.is_superuser:
        if request.POST:
            print(request.POST)
            user = User.objects.get(id=int(request.POST.get('id')))
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

                if request.POST.get('old_password'):
                    if not user.is_social_reg:
                        success = user.check_password(request.POST['old_password'])
                    else:
                        success = True
                    if success:
                        print('Old pass is good')
                        if request.POST.get('password1') == request.POST.get('password2') and request.POST.get(
                                'password1') != '' and request.POST.get('password2') != '':
                            print('Change password')
                            user.set_password(request.POST.get('password1'))
                        else:
                            print('NOT Change password')
                    else:
                        print('Old pass is bad')
                        return HttpResponseRedirect("/user/profile/edit")
                user.save()
                return HttpResponseRedirect('/cp')
            else:
                form = UpdateForm()
            return HttpResponseRedirect("/user/profile/edit")
        else:
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
        print(request.POST.get('block'))
        if request.POST.get('is_active'):
            print('disable user')
            user.is_active = False
            user.save()
            return HttpResponseRedirect('/cp')
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
            return HttpResponseRedirect('/cp')
        else:
            form = UpdateForm()
        return HttpResponseRedirect("/user/profile/edit")

def admin_create_category(request):
    print(request.POST)
    if request.POST:

        form = NewCategory(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/cp')

def admin_update_category(request):
    print(request.POST)
    if request.POST:

        form = NewCategory(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/cp')