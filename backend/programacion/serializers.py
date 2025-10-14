from rest_framework import serializers
from .models import Programa

class ProgramaSerializer(serializers.ModelSerializer):
    horario_display = serializers.ReadOnlyField()
    imagen_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Programa
        fields = [
            'id', 'nombre', 'descripcion', 'label', 
            'imagen', 'imagen_url', 'hora_inicio', 'hora_fin', 
            'horario_display', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'horario_display', 'imagen_url']
    
    def get_imagen_url(self, obj):
        if obj.imagen:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.imagen.url)
            return obj.imagen.url
        return None