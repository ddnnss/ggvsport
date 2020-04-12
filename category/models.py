from django.db import models
from pytils.translit import slugify
from random import choices
import string
from ckeditor_uploader.fields import RichTextUploadingField

class Category(models.Model):
    name = models.CharField('Категория', max_length=255, blank=False, null=True)
    name_lower = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    image = models.ImageField('Изображение (420 x 225)', upload_to='category/', blank=False, null=True)
    page_h1 = models.CharField('Тег H1 (если не указан, выводится название категории)',
                               max_length=255, blank=True, null=True)
    page_title = models.CharField('Название страницы SEO', max_length=255, blank=True, null=True)
    page_description = models.CharField('Описание страницы SEO', max_length=255, blank=True, null=True)
    page_keywords = models.TextField('Keywords SEO', blank=True, null=True)
    seo_text = RichTextUploadingField('СЕО текст на страницу', blank=True, null=True)
    views = models.IntegerField('Просмотров категории', blank=True, default=0)
    is_active = models.BooleanField('Отображается на сайте?', default=True)
    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        if not self.name_slug:
            testSlug = Category.objects.filter(name_slug=slug)
            slugRandom = ''
            if testSlug:
                slugRandom = '-' + ''.join(choices(string.ascii_lowercase + string.digits, k=2))
            self.name_slug = slug + slugRandom
        self.name_lower = self.name.lower()
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return f'Категория : {self.name}'

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class SubCategory(models.Model):
    category = models.ForeignKey(Category, blank=False, null=True, on_delete=models.SET_NULL,
                             verbose_name='Относится к ', related_name='subcat')
    name = models.CharField('Подкатегория', max_length=255, blank=False, null=True)
    name_lower = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    image = models.ImageField('Изображение (420 x 225)', upload_to='subcategory/', blank=False, null=True)
    page_h1 = models.CharField('Тег H1 (если не указан, выводится название подкатегории)',
                               max_length=255, blank=True, null=True)
    page_title = models.CharField('Название страницы SEO', max_length=255, blank=True, null=True)
    page_description = models.CharField('Описание страницы SEO', max_length=255, blank=True, null=True)
    page_keywords = models.TextField('Keywords SEO', blank=True, null=True)
    seo_text = RichTextUploadingField('СЕО текст на страницу', blank=True, null=True)
    views = models.IntegerField('Просмотров подкатегории', blank=True, default=0)
    is_active = models.BooleanField('Отображается на сайте?', default=True)
    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        if not self.name_slug:
            testSlug = SubCategory.objects.filter(name_slug=slug)
            slugRandom = ''
            if testSlug:
                slugRandom = '-' + ''.join(choices(string.ascii_lowercase + string.digits, k=2))
            self.name_slug = slug + slugRandom
        self.name_lower = self.name.lower()
        super(SubCategory, self).save(*args, **kwargs)

    def __str__(self):
        return f'Подкатегория : {self.name}'

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"