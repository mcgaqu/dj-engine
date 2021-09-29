"""
WSGI config for engine project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from .settings import SITE_NAMEX
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '%s.settings' % SITE_NAMEX)

application = get_wsgi_application()
