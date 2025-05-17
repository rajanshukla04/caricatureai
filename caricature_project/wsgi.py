

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'caricature_project.settings')

application = get_wsgi_application()  # <-- This is the standard entry point

app = application 