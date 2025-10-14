from rest_framework import serializers
from .models import NewsItem

class NewsItemSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source='nombre', max_length=10)  # Mapea label a nombre
    shortUrl = serializers.SerializerMethodField()
    
    class Meta:
        model = NewsItem
        fields = ['id', 'label', 'message', 'url', 'shortUrl', 'is_active', 'created_at']
    
    def get_shortUrl(self, obj):
        from urllib.parse import urlparse
        try:
            parsed_url = urlparse(obj.url)
            path_parts = parsed_url.path.split('/')
            filtered_parts = [part for part in path_parts if part]
            shortened_path = f"/{filtered_parts[0]}" if filtered_parts else ""
            return f"{parsed_url.netloc}{shortened_path}..."
        except:
            return obj.url
    
    def create(self, validated_data):
        # Extraer el nombre del campo label
        nombre_data = validated_data.pop('nombre', '')
        if not nombre_data:
            raise serializers.ValidationError({"label": "This field is required."})
        
        # Crear la instancia
        news_item = NewsItem.objects.create(
            nombre=nombre_data,
            message=validated_data.get('message', ''),
            url=validated_data.get('url', ''),
            is_active=validated_data.get('is_active', True)
        )
        return news_item
    
    def update(self, instance, validated_data):
        # Actualizar el nombre si viene en los datos
        nombre_data = validated_data.pop('nombre', None)
        if nombre_data is not None:
            instance.nombre = nombre_data
        
        # Actualizar otros campos
        instance.message = validated_data.get('message', instance.message)
        instance.url = validated_data.get('url', instance.url)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        
        instance.save()
        return instance