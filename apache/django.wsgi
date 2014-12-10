import os
import sys
 
path = '/srv/www'
if path not in sys.path:
    sys.path.insert(0, '/srv/www')
 
os.environ['DJANGO_SETTINGS_MODULE'] = 'gestorpsi.settings'
 
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()