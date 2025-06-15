from django import forms
from django.contrib.auth.forms import UserCreationForm
from home.models import CustomUser


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, help_text="Необязательно")
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'role']

    def clean_email(self):
        return self.cleaned_data.get('email', '')

class CreatorProfileForm(forms.ModelForm):
    banner = forms.ImageField(required=False, help_text="Необязательно")
    class Meta:
        model = CustomUser
        fields = ['avatar', 'bio', 'website', 'social_media']
        labels = {
            'avatar': 'Аватар профиля',
            'bio': 'Биография',
            'website': 'Веб-сайт',
            'social_media': 'Социальные сети'
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name']