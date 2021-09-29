"""
ASGI config for engine project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from .settings import SITE_NAMEX
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '%s.settings' % SITE_NAMEX)

application = get_asgi_application()
