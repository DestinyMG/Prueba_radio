import os
import django
from django.contrib.auth import get_user_model

# Indicar la configuración de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")  # tu carpeta de settings.py se llama 'backend'
django.setup()

User = get_user_model()

# Cambia los datos del superusuario según necesites
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "1")
    print("Superuser creado")
else:
    print("Superuser ya existe")
