#-*-coding:utf-8-*-
"""
WSGI config for docker project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
#1添加
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "docker.settings")

#2 注解
application = get_wsgi_application()
#from django.core.handlers.wsgi import WSGIHandler
#application = WSGIHandler()
