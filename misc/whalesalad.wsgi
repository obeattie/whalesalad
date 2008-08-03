# Whalesalady WSGI config
import os, sys

sys.path.extend(['/git-repos/', '/usr/local/', '/Django/Projects/'])
os.environ['DJANGO_SETTINGS_MODULE'] = 'whalesalad.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
