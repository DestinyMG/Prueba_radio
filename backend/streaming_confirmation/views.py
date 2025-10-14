from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import StreamingConfirmation
from .serializers import StreamingConfirmationSerializer

class StreamingConfirmationViewSet(viewsets.ViewSet):
    """
    ViewSet que maneja un único registro para activar/desactivar el streaming.
    """

    def get_object(self):
        obj, _ = StreamingConfirmation.objects.get_or_create(id=1)
        return obj

    def list(self, request):
        instance = self.get_object()
        serializer = StreamingConfirmationSerializer(instance)  # ✅ SIN ESPACIO
        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = StreamingConfirmationSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Deshabilitamos create, retrieve, destroy, partial_update
    def create(self, request):  
        return Response({"detail": "Método no permitido."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, pk=None):
        return Response({"detail": "Método no permitido."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        return Response({"detail": "Método no permitido."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        return Response({"detail": "Método no permitido."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)