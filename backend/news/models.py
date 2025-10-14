from django.db import models

class NewsItem(models.Model):
    # Campo nombre para escribir nombres libres (ej: "Actualidad", "Deportes", etc.)
    nombre = models.CharField(max_length=10)  # Texto libre para nombres
    
    message = models.TextField()
    url = models.URLField(max_length=500)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.nombre}: {self.message[:50]}..."