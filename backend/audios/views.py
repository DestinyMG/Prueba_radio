from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

# Create your views here.
from rest_framework import viewsets
from .models import Audio
from .serializers import AudioSerializer

class AudioViewSet(viewsets.ModelViewSet):
    queryset = Audio.objects.all().order_by('play_date')
    serializer_class = AudioSerializer
    # permission_classes = [IsAuthenticated]

