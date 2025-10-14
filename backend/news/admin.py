from django.contrib import admin
from .models import NewsItem

@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'message', 'url', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['nombre', 'message', 'url']
    list_editable = ['is_active']