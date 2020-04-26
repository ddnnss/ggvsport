from django.forms import ModelForm

from .models import *


class NewCategory(ModelForm):
    class Meta:
        model = Category
        fields = ('name_ru',
                  'name_en',
                  'name_az',
                  'image',
                  'page_title_ru',
                  'page_title_en',
                  'page_title_az',
                  'page_description_ru',
                  'page_description_en',
                  'page_description_az',
                  'page_keywords_ru',
                  'page_keywords_en',
                  'page_keywords_az',
                  'seo_text_ru',
                  'seo_text_en',
                  'seo_text_az'
                  )

class NewSubCategory(ModelForm):
    class Meta:
        model = SubCategory
        fields = (
                  'name_ru',
                  'name_en',
                  'name_az',
                  'image',
                  'page_title_ru',
                  'page_title_en',
                  'page_title_az',
                  'page_description_ru',
                  'page_description_en',
                  'page_description_az',
                  'page_keywords_ru',
                  'page_keywords_en',
                  'page_keywords_az',
                  'seo_text_ru',
                  'seo_text_en',
                  'seo_text_az'
                  )

class UpdateCategory(ModelForm):
    class Meta:
        model = Category
        fields = ('name_ru',
                  'name_en',
                  'name_az',
                  'image',
                  'page_title_ru',
                  'page_title_en',
                  'page_title_az',
                  'page_description_ru',
                  'page_description_en',
                  'page_description_az',
                  'page_keywords_ru',
                  'page_keywords_en',
                  'page_keywords_az',
                  'seo_text_ru',
                  'seo_text_en',
                  'seo_text_az'
                  )

class UpdateSubCategory(ModelForm):
    class Meta:
        model = SubCategory
        fields = ('name_ru',
                  'name_en',
                  'name_az',
                  'image',
                  'page_title_ru',
                  'page_title_en',
                  'page_title_az',
                  'page_description_ru',
                  'page_description_en',
                  'page_description_az',
                  'page_keywords_ru',
                  'page_keywords_en',
                  'page_keywords_az',
                  'seo_text_ru',
                  'seo_text_en',
                  'seo_text_az'
                  )
