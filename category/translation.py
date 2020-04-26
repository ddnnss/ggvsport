from modeltranslation.translator import register, TranslationOptions
from .models import Category, SubCategory


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'seo_text','page_h1','page_title','page_description','page_keywords',)


@register(SubCategory)
class SubCategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'seo_text','page_h1','page_title','page_description','page_keywords',)


