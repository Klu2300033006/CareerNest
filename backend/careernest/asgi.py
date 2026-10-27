"""
ASGI config for CareerNest project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'careernest.settings')
application = get_asgi_application()
