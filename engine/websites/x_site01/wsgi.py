"""
WSGI config for engine project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from .settings import SITE_NAME, BASE_NAME
# import pdb; pdb.set_trace()

if "dj%s" % SITE_NAME == BASE_NAME:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '%s.settings' % SITE_NAME)
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'websites.%s.settings' % SITE_NAME)
# os.environ['NUM_ADMIN_SITE'] = "2"

# os.environ['NUM_ADMIN_SITE'] = "2"

application = get_wsgi_application()
