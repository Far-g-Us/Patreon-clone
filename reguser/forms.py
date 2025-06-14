from django import forms
from django.contrib.auth.forms import UserCreationForm
from home.models import CustomUser


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']


class CreatorProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['bio', 'avatar', 'website', 'social_media']