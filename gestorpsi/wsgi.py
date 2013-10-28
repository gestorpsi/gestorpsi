import os
import sys

from django.core.handlers.wsgi import WSGIHandler

sys.path = ['/home/redepsi/w/gestorpsi_demo/git.gestorpsi.com.br/gestorpsi', '/home/redepsi/lib/python2.7'] + sys.path


os.environ['DJANGO_SETTINGS_MODULE'] = 'gestorpsi.settings'
application = WSGIHandler()
