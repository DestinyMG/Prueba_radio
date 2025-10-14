from django.db import models

class Programa(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    label = models.CharField(max_length=20)
    imagen = models.ImageField(upload_to='programas/', blank=True, null=True)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['hora_inicio']
        verbose_name = 'Programa'
        verbose_name_plural = 'Programas'
    
    def __str__(self):
        return f"{self.nombre} ({self.hora_inicio} - {self.hora_fin})"
    
    @property
    def horario_display(self):
        return f"{self.hora_inicio.strftime('%I:%M %p')} - {self.hora_fin.strftime('%I:%M %p')}"