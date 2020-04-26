from modeltranslation.translator import register, TranslationOptions
from .models import *


@register(SeoTag)
class SeoTagTranslationOptions(TranslationOptions):
    fields = ( 'index_h1','index_title','index_description','index_keywords','index_seo',)


@register(Month)
class MonthTranslationOptions(TranslationOptions):
    fields = ('name',)



