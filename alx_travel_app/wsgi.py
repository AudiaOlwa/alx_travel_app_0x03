import os
from django.core.wsgi import get_wsgi_application

# Remplace 'alx_travel_app_0x01' par le nom exact de ton dossier de projet
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_travel_app_0x02.settings')

application = get_wsgi_application()
