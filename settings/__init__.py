# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
import os, sys
from django.core.management import call_command
from django.core.exceptions import ImproperlyConfigured

ENV = os.getenv('DJANGO_ENV', 'development')

if ENV == 'production':
    from .prod import *
elif ENV == 'development':
    from .dev import *
else:
    raise ImproperlyConfigured("DJANGO_ENV environment variable is not set or invalid")

