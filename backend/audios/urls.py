from rest_framework import routers
from .views import AudioViewSet

router = routers.DefaultRouter()
router.register(r'audios', AudioViewSet, basename='audio')

urlpatterns = router.urls
