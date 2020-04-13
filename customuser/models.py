from .utils import create_random_string
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from category.models import Category



class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):

    username = None
    avatar = models.ImageField('Фото', upload_to='user',blank=True,null=True)
    photo = models.CharField('VK аватар', max_length=255, blank=True, null=True)
    first_name = models.CharField('Имя', max_length=50, blank=True, null=True)
    last_name = models.CharField('Фамилия', max_length=50, blank=True, null=True)
    genre = models.BooleanField('Пол мужской?',blank=True, null=True)
    nickname = models.CharField('Ник', max_length=50, blank=True, null=True)
    email = models.EmailField('Эл. почта', blank=True, null=True, unique=True)
    birthday_day = models.CharField('День рождения',max_length=10, blank=True, null=True)
    birthday_month = models.CharField('Месяц рождения',max_length=10, blank=True, null=True)
    birthday_year = models.CharField('Год рождения',max_length=10, blank=True, null=True)
    fav_category1 = models.ForeignKey(Category,blank=True,null=True,on_delete=models.SET_NULL,verbose_name='Категория1',
                                      related_name='fav_category1')
    fav_category2 = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL,
                                      verbose_name='Категория2',
                                      related_name='fav_category2')
    fav_category3 = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL,
                                      verbose_name='Категория3',
                                      related_name='fav_category3')
    fav_category4 = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL,
                                      verbose_name='Категория4',
                                      related_name='fav_category4')
    is_social_reg = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        if self.nickname:
            return self.nickname
        else:
            return self.email

    def get_name(self):
        if self.last_name:
            return f'{self.last_name} {self.first_name}'
        else:
            if self.first_name:
                return f'{self.first_name}'
            else:
                return 'Имя не установлено'

    def get_nickname(self):
        if self.nickname:
            return self.nickname
        else:
            return 'Ник не установлен'

    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        elif self.photo:
            return self.photo
        else:
            return '/static/img/user.jpg'




