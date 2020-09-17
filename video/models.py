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
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
                              verbose_name='Загрузил')
    category = models.ForeignKey(Category,blank=True,null=True,on_delete=models.CASCADE,verbose_name='Категория')
    subcategory = models.ForeignKey(SubCategory,blank=False,null=True,on_delete=models.CASCADE,verbose_name='Подкатегория')
    name = models.CharField('Название', max_length=255, blank=False, null=True)
    name_lower = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    image = models.ImageField('Изображение (550 x 300)', upload_to='video_thumb/', blank=False, null=True)
    file = models.FileField('Видое', upload_to='videos/', blank=True, null=True)
    description = models.TextField('Описание', blank=True, null=True)
    views = models.IntegerField('Просмотров', blank=True, default=0)
    likes = models.IntegerField('Лайков', default=0)
    dislikes = models.IntegerField('Дизлайков', default=0)
    duration = models.IntegerField('Длительность', default=0)
    liked_by_users = models.TextField(blank=True, null=True,default='')
    disliked_by_users = models.TextField(blank=True, null=True,default='')
    comments = models.IntegerField('Комментариев', default=0)
    is_active = models.BooleanField('Отображается на сайте?', default=True)
    is_moderated = models.BooleanField('Проверено?', default=False)
    is_now_watching = models.BooleanField('Смотрят?', default=False)
    start_watch = models.DateTimeField(blank=True,null=True)
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
        if self.user.is_superuser:
            self.is_moderated = True
        super(Video, self).save(*args, **kwargs)
    def get_absolute_url(self):
        return f'/video/{self.name_slug}'

    def __str__(self):
        return f'Видео : {self.name}'

    def get_video_image(self):
        if self.image and self.image!='':
            return self.image.url
        else:
            return '/static/img/video_img.jpg'

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"



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
    liked_by_users = models.TextField(blank=True, null=True, default='')
    disliked_by_users = models.TextField(blank=True, null=True, default='')

    def __str__(self):
        return f'Комментарий пользователя : {self.user.email}'

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

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
    user = models.ManyToManyField(User, blank=True,  verbose_name='Пользователь')
    video = models.ForeignKey(Video, blank=False, null=True, on_delete=models.CASCADE,
                             verbose_name='Видео')
    def __str__(self):
        return f'Реакция на видео (Лайк) : {self.video.id}'
    class Meta:
        verbose_name = "Реакция на видео (Лайк)"
        verbose_name_plural = "Реакция на видео (Лайк)"


class VideoDislike(models.Model):
    user = models.ManyToManyField(User, blank=True,  verbose_name='Пользователь')
    video = models.ForeignKey(Video, blank=False, null=True, on_delete=models.CASCADE,
                              verbose_name='Видео')
    def __str__(self):
        return f'Реакция на видео (ДизЛайк) : {self.video.id}'

    class Meta:
        verbose_name = "Реакция на видео (ДизЛайк)"
        verbose_name_plural = "Реакция на видео (ДизЛайк)"


class VideoHistory(models.Model):
    video = models.ManyToManyField(Video, blank=True, verbose_name='Видео')
    user = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE,
                              verbose_name='Пользователь')
    def __str__(self):
        return f'История видео : {self.video.id}'
    class Meta:
        verbose_name = "История видео"
        verbose_name_plural = "История видео"


def video_post_save(sender, instance, created, **kwargs):
    if created:
        blob = BytesIO()
        threshold = 100
        import cv2
        print(instance.file.url)
        bd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        vcap = cv2.VideoCapture(bd + instance.file.url)
        fps = vcap.get(cv2.CAP_PROP_FPS)  # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
        frame_count = int(vcap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps
        print(duration)
        success, image = vcap.read()
        cv2.imwrite(f'{instance.name_slug}.jpg', image)  # save frame as JPEG file
        instance.image.save(
                f'{instance.name_slug}.jpg',
                File(open(f'{bd}/{instance.name_slug}.jpg', 'rb'))
            )
        instance.duration=round(duration)
        instance.save()
        os.remove(f'{bd}/{instance.name_slug}.jpg')


        # res, im_ar = vcap.read()

        # try:
        #     while im_ar.mean() < threshold and res:
        #         res, im_ar = vcap.read()
        #     im_ar = cv2.resize(im_ar, (770, 410), 0, 0, cv2.INTER_LINEAR)
        #     cv2.imwrite(f'{instance.name_slug}.jpg', im_ar)
        #     instance.image.save(
        #         f'{instance.name_slug}.jpg',
        #         File(open(f'{bd}/{instance.name_slug}.jpg', 'rb'))
        #     )
        #     instance.duration=round(duration)
        #     instance.save()
        #     os.remove(f'{bd}/{instance.name_slug}.jpg')
        # except:
        #     pass



post_save.connect(video_post_save, sender=Video)