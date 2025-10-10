from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Endpoint para login (obtener access + refresh token)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Endpoint para refrescar el access token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
