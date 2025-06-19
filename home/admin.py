from django.contrib import admin
from .models import *

@admin.register(DownloadHistory)
class DownloadHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'downloaded_at')
    list_filter = ('downloaded_at', 'content')
    search_fields = ('user__username', 'content__title')