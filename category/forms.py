from django.forms import ModelForm

from .models import *


class NewCategory(ModelForm):


    class Meta:
        model = Category
        fields = ('name', 'image', 'page_title','page_description','page_keywords','seo_text' )


