from django.db import models

# Create your models here.

class StreamingConfirmation(models.Model):
    activate = models.BooleanField(default=False)

    def __str__(self):
        return "Streaming Activo" if self.activate else "Streaming Inactivo"
