from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class SeoTag(models.Model):
    index_h1 = models.CharField('h1 главной', max_length=255,blank=True,null=True)
    index_title = models.CharField('Title главной', max_length=255,blank=True,null=True)
    index_description = models.TextField('description главной', blank=True,null=True)
    index_keywords = models.TextField('keywords главной', blank=True,null=True)
    index_seo = RichTextUploadingField('СЕО текст главной', blank=True, null=True)

class Month(models.Model):
    name = models.CharField('Название месяца', max_length=255,blank=True,null=True)


