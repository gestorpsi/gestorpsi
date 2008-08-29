from django.conf.urls.defaults import *

urlpatterns = patterns('gestorpsi.client.views',
    (r'^$', 'index'), #list objects
    (r'^add/$', 'form'), #new object form
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', 'form'),
    (r'^save/$', 'save'), #save new object
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/save/$', 'save'),  #update object
    (r'^(?P<object_id>\d+)/delete/$', 'delete'), # delete object
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/delete/$', 'delete'),  #delete object
)