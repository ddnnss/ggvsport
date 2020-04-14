from django.db import models
from django.db.models.signals import post_save
from pytils.translit import slugify
from random import choices
import string
from customuser.models import User
from category.models import *
from io import BytesIO
from django.core.files import File
import os
class Video(models.Model):
    user = models.ForeignKey(User, blank=False, null=True, on_delete=models.SET_NULL,
                              verbose_name='Загрузил')
    category = models.ForeignKey(Category,blank=True,null=True,on_delete=models.SET_NULL,verbose_name='Категория')
    subcategory = models.ForeignKey(SubCategory,blank=False,null=True,on_delete=models.SET_NULL,verbose_name='Подкатегория')
    name = models.CharField('Название', max_length=255, blank=False, null=True)
    name_lower = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    image = models.ImageField('Изображение (550 x 300)', upload_to='video_thumb/', blank=False, null=True)
    file = models.FileField('Видое', upload_to='videos/', blank=False, null=True)
    description = models.TextField('Описание', blank=True, null=True)
    views = models.IntegerField('Просмотров', blank=True, default=0)
    likes = models.IntegerField('Лайков', default=0)
    dislikes = models.IntegerField('Дизлайков', default=0)
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


        super(Video, self).save(*args, **kwargs)

    def __str__(self):
        return f'Видео : {self.name}'

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"

    def get_like_count(self):
        all_likes = VideoLike.objects.filter(video=self,is_like=True)
        return all_likes.count()

    def get_dislike_count(self):
        all_likes = VideoLike.objects.filter(video=self,is_dislike=True)
        return all_likes.count()

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
    video = models.ForeignKey(Video, blank=False, null=True, on_delete=models.CASCADE,
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
    def get_created_time(self):
        return f'{self.created_at.strftime("%d.%m.%Y,%H:%M:%S")}'

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

class VideoLike(models.Model):
    user = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    video = models.ForeignKey(Video, blank=False, null=True, on_delete=models.CASCADE,
                             verbose_name='Видео')
    is_like = models.BooleanField('Лайк?', blank=True, null=True, default=None)
    is_dislike = models.BooleanField('ДизЛайк?', blank=True, null=True, default=None)

    def __str__(self):
        return f'Реакция на видео : {self.comment.id}'

    class Meta:
        verbose_name = "Реакция на видео"
        verbose_name_plural = "Реакция на видео"

def video_post_save(sender, instance, created, **kwargs):

    if created:
        blob = BytesIO()
        threshold = 100
        import cv2
        print(instance.file.url)
        bd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        vcap = cv2.VideoCapture(bd + instance.file.url)
        res, im_ar = vcap.read()
        while im_ar.mean() < threshold and res:
            res, im_ar = vcap.read()
        im_ar = cv2.resize(im_ar, (770, 410), 0, 0, cv2.INTER_LINEAR)
        cv2.imwrite(f'{instance.name_slug}.jpg', im_ar)
        instance.image.save(
            f'{instance.name_slug}.jpg',
            File(open(f'{bd}/{instance.name_slug}.jpg', 'rb'))
        )
        os.remove(f'{bd}/{instance.name_slug}.jpg')


post_save.connect(video_post_save, sender=Video)