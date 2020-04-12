from django.contrib import admin
from .models import *
admin.site.register(Video)
admin.site.register(FavoriteVideo)
admin.site.register(CommentVideo)
admin.site.register(CommentLike)

