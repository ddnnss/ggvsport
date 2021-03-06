from django.forms import ModelForm


from .models import Video


class CreateVideo(ModelForm):
    class Meta:
        model = Video
        fields = ('name', 'file', 'description', )


class EditVideo(ModelForm):
    class Meta:
        model = Video
        fields = ('name', 'file', 'description', )