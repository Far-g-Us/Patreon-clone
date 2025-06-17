from django import forms
from django.contrib.auth.forms import UserCreationForm
from home.models import CustomUser


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, help_text="Необязательно")
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        widget=forms.RadioSelect,
        label='Тип аккаунта'
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'role']

    def clean_email(self):
        return self.cleaned_data.get('email', '')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user

# class CreatorProfileForm(forms.ModelForm):
#     banner = forms.ImageField(required=False, help_text="Необязательно")
#     class Meta:
#         model = CustomUser
#         fields = ['avatar', 'bio', 'website', 'social_media']
#         labels = {
#             'avatar': 'Аватар профиля',
#             'bio': 'Биография',
#             'website': 'Веб-сайт',
#             'social_media': 'Социальные сети'
#         }
#         widgets = {
#             'bio': forms.Textarea(attrs={'rows': 4}),
#         }
#
# class UserSettingsForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ['email', 'first_name', 'last_name']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'avatar',
            'banner',
            'first_name',
            'last_name',
            'email',
            'bio',
            'website',
            'social_media'
        ]
        labels = {
            'avatar': 'Аватар',
            'banner': 'Баннер профиля',
            'bio': 'Биография',
            'website': 'Веб-сайт',
            'social_media': 'Социальные сети'
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем email обязательным только при первом сохранении
        if self.instance and self.instance.email:
            self.fields['email'].required = False

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Проверка уникальности email
        if CustomUser.objects.exclude(id=self.instance.id).filter(email=email).exists():
            raise forms.ValidationError("Этот email уже используется")
        return email