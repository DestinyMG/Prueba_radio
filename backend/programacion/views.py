from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Programa
from .serializers import ProgramaSerializer

class ProgramaViewSet(viewsets.ModelViewSet):
    queryset = Programa.objects.filter(is_active=True)
    serializer_class = ProgramaSerializer
    
    def get_queryset(self):
        return Programa.objects.filter(is_active=True).order_by('hora_inicio')
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
    
    @action(detail=False, methods=['get'])
    def activos(self, request):
        programas = self.get_queryset()
        serializer = self.get_serializer(programas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def hoy(self, request):
        programas = self.get_queryset()
        serializer = self.get_serializer(programas, many=True)
        return Response(serializer.data)