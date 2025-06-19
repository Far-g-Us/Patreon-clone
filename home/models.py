from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
import os


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
    # content_image = models.ImageField(upload_to='content_image/', blank=True, null=True)
    description = models.TextField()
    file = models.FileField(upload_to='content_files/')  # Основное поле для файлов
    file_size = models.PositiveIntegerField(
        blank=True,
        null=True,
        editable=False,
        verbose_name="Размер файла (байты)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)  # Бесплатный контент
    download_count = models.IntegerField(default=0)

    @property
    def file_type(self):
        if self.file:
            extension = self.file.name.split('.')[-1].lower()
            if extension in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
                return 'image'
            elif extension in ['mp4', 'avi', 'mov', 'mkv', 'webm']:
                return 'video'
            elif extension in ['pdf', 'doc', 'docx', 'txt']:
                return 'document'
            elif extension in ['mp3', 'wav', 'ogg']:
                return 'audio'
        return 'other'

    def save(self, *args, **kwargs):
        # Автоматически вычисляем размер файла при сохранении
        if self.file:
            self.file_size = self.file.size

        # Удаляем старый файл при обновлении
        if self.pk:
            old_instance = Content.objects.get(pk=self.pk)
            if old_instance.file and old_instance.file != self.file:
                old_instance.file.delete(save=False)

        super().save(*args, **kwargs)

class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.tier.name}"


class DownloadHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='download_history'
    )
    content = models.ForeignKey(
        Content,
        on_delete=models.CASCADE,
        related_name='download_history'
    )
    downloaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-downloaded_at']
        verbose_name = 'История скачивания'
        verbose_name_plural = 'История скачиваний'

    def __str__(self):
        return f"{self.user.username} скачал {self.content.title}"