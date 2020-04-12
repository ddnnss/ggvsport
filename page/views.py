from django.shortcuts import render, get_object_or_404
from category.models import *

def index(request):
    return render(request, 'page/index.html', locals())

def category(request,slug):
    category = get_object_or_404(Category, name_slug=slug)
    return render(request, 'page/category.html', locals())

