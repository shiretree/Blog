"""
WSGI config for blog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

profile = os.environ.get('blog_PROFILE','develop')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.setting.%s" %profile)

application = get_wsgi_application()