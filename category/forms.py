from django.forms import ModelForm

from .models import *


class NewCategory(ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'image', 'page_title','page_description','page_keywords','seo_text' )

class NewSubCategory(ModelForm):
    class Meta:
        model = SubCategory
        fields = ('category','name', 'image', 'page_title','page_description','page_keywords','seo_text' )

class UpdateCategory(ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'image', 'page_title','page_description','page_keywords','seo_text' )

class UpdateSubCategory(ModelForm):
    class Meta:
        model = SubCategory
        fields = ('name', 'image', 'page_title','page_description','page_keywords','seo_text' )
