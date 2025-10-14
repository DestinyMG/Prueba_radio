from django.contrib import admin
from .models import Programa

@admin.register(Programa)
class ProgramaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'label', 'hora_inicio', 'hora_fin', 'is_active']
    list_filter = ['is_active', 'created_at', 'label']
    search_fields = ['nombre', 'descripcion', 'label']
    list_editable = ['is_active']
    ordering = ['hora_inicio']