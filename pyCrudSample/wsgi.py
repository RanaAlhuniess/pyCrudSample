"""
WSGI config for pyCrudSample project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pyCrudSample.settings')

application = get_wsgi_application()

if not User.objects.filter(username="admin").first():
    User.objects.create_superuser('admin', 'admin@admin.com', 'admin')