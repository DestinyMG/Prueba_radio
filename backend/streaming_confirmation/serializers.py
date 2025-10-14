from rest_framework import serializers
from .models import StreamingConfirmation

class StreamingConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamingConfirmation
        fields = ['id', 'activate']
