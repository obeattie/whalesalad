# This file is used to integrade Django and mod_wsgi

import os, sys
sys.path.append('/usr/local/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'whalesalad.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()