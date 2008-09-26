from django.conf.urls.defaults import *

urlpatterns = patterns('gestorpsi.device.views',
    (r'^$', 'index'), # list objects
    (r'^add/$', 'form'), # new object form
    #(r'^add/(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', 'form'), # edit object form
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', 'form'), # edit object form
   
    (r'^save/$', 'save'), # save new object
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/save/$', 'save'), # update object
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/delete/$', 'delete'), # delete object
)

