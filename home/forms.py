from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from home.models import Content


def validate_file_size(value):
    if value.size > settings.MAX_FILE_SIZE:
        raise ValidationError('Файл слишком большой!')


class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['title', 'file', 'description', 'tier']

    file = forms.FileField(validators=[validate_file_size])