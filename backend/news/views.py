from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import NewsItem
from .serializers import NewsItemSerializer

class NewsItemViewSet(viewsets.ModelViewSet):
    queryset = NewsItem.objects.filter(is_active=True)
    serializer_class = NewsItemSerializer
    
    def get_queryset(self):
        return NewsItem.objects.filter(is_active=True).order_by('-created_at')
    
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
    
    @action(detail=False, methods=['get'])
    def active_news(self, request):
        news_items = self.get_queryset()
        serializer = self.get_serializer(news_items, many=True)
        return Response(serializer.data)