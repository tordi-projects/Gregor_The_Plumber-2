"""WSGI config for the Luke The Plumber project."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'luke_plumber.settings')

application = get_wsgi_application()
