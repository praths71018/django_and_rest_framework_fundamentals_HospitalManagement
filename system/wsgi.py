"""
WSGI config for system project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import newrelic.agent

newrelic.agent.initialize('/Users/prathamshetty/Desktop/Shadowfax/Hospital/newrelic.ini')  # Update the path to your newrelic.ini file

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'system.settings')

application = get_wsgi_application()
