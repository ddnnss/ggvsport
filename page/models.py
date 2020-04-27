from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class SeoTag(models.Model):
    index_h1 = models.CharField('h1 главной', max_length=255,blank=True,null=True)
    index_title = models.CharField('Title главной', max_length=255,blank=True,null=True)
    index_description = models.TextField('description главной', blank=True,null=True)
    index_keywords = models.TextField('keywords главной', blank=True,null=True)
    index_seo = RichTextUploadingField('СЕО текст главной', blank=True, null=True)
    podcast_title = models.CharField('Title подкастов', max_length=255, blank=True, null=True)
    podcast_description = models.TextField('description подкастов', blank=True, null=True)
    podcast_keywords = models.TextField('keywords подкастов', blank=True, null=True)
    podcast_seo = RichTextUploadingField('СЕО текст подкастов', blank=True, null=True)
    recomended_title = models.CharField('Title рекомендаций', max_length=255, blank=True, null=True)
    recomended_description = models.TextField('description рекомендаций', blank=True, null=True)
    recomended_keywords = models.TextField('keywords рекомендаций', blank=True, null=True)
    recomended_seo = RichTextUploadingField('СЕО текст рекомендаций', blank=True, null=True)
    trends_title = models.CharField('Title трендов', max_length=255, blank=True, null=True)
    trends_description = models.TextField('description трендов', blank=True, null=True)
    trends_keywords = models.TextField('keywords трендов', blank=True, null=True)
    trends_seo = RichTextUploadingField('СЕО текст трендов', blank=True, null=True)

class Month(models.Model):
    name = models.CharField('Название месяца', max_length=255,blank=True,null=True)


