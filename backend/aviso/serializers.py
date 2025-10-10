from rest_framework import serializers
from .models import Aviso
from audios.models import Audio


class AvisoSerializer(serializers.ModelSerializer):
    # Solo mostramos el archivo (mp3)
    audio_file = serializers.FileField(source="audio.file", read_only=True)

    # Para escritura seguimos permitiendo pasar un audio_id
    audio_id = serializers.PrimaryKeyRelatedField(
        queryset=Audio.objects.all(),
        source="audio",   # apunta al campo audio en el modelo
        write_only=True,
        required=False
    )

    class Meta:
        model = Aviso
        fields = ['activo', 'audio_file', 'audio_id']

    def update(self, instance, validated_data):
        # Si explícitamente desactivamos el aviso, limpiar el audio
        if 'activo' in validated_data and validated_data['activo'] is False:
            instance.audio = None
            instance.activo = False

        # Si viene un audio_id y activo es True, actualizar
        if 'audio' in validated_data and validated_data.get('activo', instance.activo):
            instance.audio = validated_data['audio']
            instance.activo = True

        # Si solo se manda activo=True pero no audio_id, mantener el audio existente
        if 'activo' in validated_data and validated_data['activo'] is True and 'audio' not in validated_data:
            instance.activo = True

        instance.save()
        return instance
