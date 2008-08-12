from django.conf.urls.defaults import *

urlpatterns = patterns('gestorpsi.psychologist.views',
    (r'^$', 'index'),    
    (r'^add$', 'form'),
    (r'^(?P<object_id>\d+)/$', 'form'),
    (r'^save/$', 'save'),
    (r'^(?P<object_id>\d+)/save/$', 'save'),
    (r'^(?P<object_id>\d+)/delete/$', 'delete'),
)