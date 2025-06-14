from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'Regular User'),
        ('creator', 'Content Creator'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    banner = models.ImageField(upload_to='banner/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Для создателей
    website = models.URLField(blank=True, null=True)
    social_media = models.CharField(max_length=255, blank=True, null=True)

    def is_creator(self):
        return self.role == 'creator'

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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)