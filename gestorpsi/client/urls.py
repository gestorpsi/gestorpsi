from django.conf.urls.defaults import *

urlpatterns = patterns('gestorpsi.client.views',
    (r'^$', 'index'), # list objects
    (r'^add/$', 'form'), # new object form
    (r'^(?P<object_id>\d+)/$', 'form'), # edit object form
    (r'^save/$', 'save'), # save new object
    (r'^(?P<object_id>\d+)/save/$', 'save'), # update object
    (r'^(?P<object_id>\d+)/delete/$', 'delete'), # delete object
)