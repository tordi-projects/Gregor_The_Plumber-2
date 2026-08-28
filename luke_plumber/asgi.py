"""ASGI config for the Luke The Plumber project."""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'luke_plumber.settings')

application = get_asgi_application()
