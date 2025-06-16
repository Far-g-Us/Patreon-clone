from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'Regular User'),
        ('creator', 'Content Creator'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    ###
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(default='avatars/default_pic.png', upload_to='avatars/', blank=True, null=True)
    banner = models.ImageField(default='banners/default_banner.jpg', upload_to='banner/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Для создателей
    website = models.URLField(blank=True, null=True)
    social_media = models.CharField(max_length=255, blank=True, null=True)

    @property
    def is_creator(self) -> bool:
        return self.role == 'creator'

    @property
    def is_regular_user(self):
        return self.role == 'user'

    def get_absolute_url(self):
        if self.is_creator:
            return reverse('profile', kwargs={'user_id': self.id})
        return reverse('home')

class Tier(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'creator'},  # Важно: только создатели!
        related_name='tiers'
    )
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()

class Content(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'creator'}  # Важно: только создатели!
    )
    tier = models.ForeignKey(Tier, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='content_files/')  # Основное поле для файлов
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)  # Бесплатный контент

class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions'  # Добавьте это!
    )
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.tier.name}"