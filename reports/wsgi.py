"""
WSGI config for reports project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
import socket

env = socket.gethostname()

from django.core.wsgi import get_wsgi_application

settings_file = "reports.settings_" + env

os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_file)

application = get_wsgi_application()