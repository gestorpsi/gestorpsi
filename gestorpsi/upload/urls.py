from django.conf.urls.defaults import *

urlpatterns = patterns('gestorpsi.upload.views',
    (r'^send/$', 'send'), 
)
