from django.urls import path
from .views import StreamingConfirmationViewSet

streaming_view = StreamingConfirmationViewSet.as_view({
    'get': 'list',
    'put': 'update',
})

urlpatterns = [
    path('', streaming_view, name='streaming-confirmation'),
]
