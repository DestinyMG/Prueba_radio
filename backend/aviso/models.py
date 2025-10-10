# aviso/models.py
from django.db import models
from audios.models import Audio

class Aviso(models.Model):
    activo = models.BooleanField(default=False)
    audio = models.ForeignKey(Audio, on_delete=models.SET_NULL, null=True, blank=True)
