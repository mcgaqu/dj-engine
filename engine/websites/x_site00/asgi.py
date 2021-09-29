"""
ASGI config for engine project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from .setconf import SITE_NAME, BASE_NAME
if "dj%s" % SITE_NAME == BASE_NAME:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '%s.settings' % SITE_NAME)
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'websites.%s.settings' % SITE_NAME)
os.environ['NUM_ADMIN_SITE'] = 2

application = get_asgi_application()
