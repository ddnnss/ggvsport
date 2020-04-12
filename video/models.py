from django.db import models
from pytils.translit import slugify
from random import choices
import string
from customuser.models import User
from category.models import *

class Video(models.Model):
    user = models.ForeignKey(User, blank=False, null=True, on_delete=models.SET_NULL,
                              verbose_name='Загрузил')
    category = models.ForeignKey(Category,blank=True,null=True,on_delete=models.SET_NULL,verbose_name='Категория')
    subcategory = models.ForeignKey(SubCategory,blank=False,null=True,on_delete=models.SET_NULL,verbose_name='Подкатегория')
    name = models.CharField('Название', max_length=255, blank=False, null=True)
    name_lower = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    image = models.ImageField('Изображение (420 x 225)', upload_to='category/', blank=False, null=True)
    file = models.FileField('Видое', upload_to='videos/', blank=False, null=True)
    description = models.TextField('Описание', blank=True, null=True)
    views = models.IntegerField('Просмотров', blank=True, default=0)
    likes = models.IntegerField('Лайков', default=0)
    comments = models.IntegerField('Комментариев', default=0)
    is_active = models.BooleanField('Отображается на сайте?', default=True)
    is_moderated = models.BooleanField('Проверено?', default=True)
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)
    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        if not self.name_slug:
            testSlug = Video.objects.filter(name_slug=slug)
            slugRandom = ''
            if testSlug:
                slugRandom = '-' + ''.join(choices(string.ascii_lowercase + string.digits, k=2))
            self.name_slug = slug + slugRandom
        self.name_lower = self.name.lower()
        self.category = self.subcategory.category
        super(Video, self).save(*args, **kwargs)

    def __str__(self):
        return f'Видео : {self.name}'

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"
    def check_favotites(self):
        print(FavoriteVideo.objects.filter(user=self.user))

class FavoriteVideo(models.Model):
    user = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    videos = models.ManyToManyField(Video)

    def __str__(self):
        return f'Избранное пользователя : {self.user.email}'

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"


class CommentVideo(models.Model):
    user = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    videos = models.ForeignKey(Video, blank=False, null=True, on_delete=models.CASCADE,
                             verbose_name='Видео')
    comment = models.TextField('Комментарий', blank=False,null=True)
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)
    likes = models.IntegerField('Лайков', default=0)
    dislikes = models.IntegerField('Дизлайков', default=0)

    def __str__(self):
        return f'Комментарий пользователя : {self.user.email}'

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
    def get_likes(self):
        print(self.commentlike_set.all())

class CommentLike(models.Model):
    user = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    comment = models.ForeignKey(CommentVideo, blank=False, null=True, on_delete=models.CASCADE,
                             verbose_name='Комментарий')
    is_like = models.BooleanField('Лайк?', blank=True, null=True)



    def __str__(self):
        return f'Реакция на комментарий : {self.comment.id}'

    class Meta:
        verbose_name = "Реакция на комментарий"
        verbose_name_plural = "Реакция на комментарий"