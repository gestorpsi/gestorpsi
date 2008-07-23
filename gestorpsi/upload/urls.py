from django.conf.urls.defaults import *

urlpatterns = patterns('gestorpsi.upload.views',
    (r'^client/$', 'upload_client'), 
)
