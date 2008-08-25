from django.conf.urls.defaults import *

urlpatterns = patterns('gestorpsi.careprofessional.views',
    # unnecessary views by now
    # will be removed soon
    (r'^$', 'index'),    
    (r'^add$', 'form'),
    (r'^(?P<object_id>\d+)/$', 'form'),
    (r'^save/$', 'save'),
    (r'^(?P<object_id>\d+)/save/$', 'save'),
    (r'^(?P<object_id>\d+)/delete/$', 'delete'),
)