from django.conf.urls.defaults import *

urlpatterns = patterns('gestorpsi.device.views',
    ( r'^$', 'index' ),
    ( r'^form/(\d+)$', 'form' ),
    (r'^save/(\d+)$', 'save'),
    (r'^delete/(\d+)$', 'delete'), 
)