from django.conf.urls.defaults import *

urlpatterns = patterns('gestorpsi.person.views',
    (r'^$', 'index'),
    (r'^add$', 'form'),
    (r'^(?P<client_id>\d+)/$', 'form'),
    (r'^save/$', 'save'),
    (r'^(?P<client_id>\d+)/save/$', 'save'),
    (r'^(?P<client_id>\d+)/delete/$', 'delete'),
)