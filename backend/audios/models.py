from django.db import models
import os
from django.dispatch import receiver

class Audio(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="audios/")
    play_date = models.DateTimeField()

    def __str__(self):
        return self.title


# 👇 Esto elimina el archivo físico al borrar el registro
@receiver(models.signals.post_delete, sender=Audio)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
