from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from home.models import Content


# def validate_file_size(value):
#     if value.size > settings.MAX_FILE_SIZE:
#         raise ValidationError('Файл слишком большой!')
#
#
# class ContentForm(forms.ModelForm):
#     class Meta:
#         model = Content
#         fields = ['title', 'file', 'description', 'tier']
#
#     file = forms.FileField(validators=[validate_file_size])

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['title', 'description', 'file', 'is_public', 'tier']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        self.creator = kwargs.pop('creator', None)
        super().__init__(*args, **kwargs)

        # Ограничиваем выбор тарифа только тарифами текущего создателя
        if self.creator and self.creator.is_creator:
            self.fields['tier'].queryset = self.creator.tiers.all()

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file and file.size > settings.MAX_FILE_SIZE:
            raise ValidationError("Файл слишком большой. Максимальный размер 500MB")
        return file