from django.conf.urls.defaults import *

urlpatterns = patterns('gestorpsi.client.views',
    (r'^$', 'index'),
    (r'^add$', 'add'),
    (r'^(?P<client_id>\d+)/$', 'detail'),
    (r'^save$', 'save'),
    (r'^update$', 'update'),
    (r'^(?P<client_id>\d+)/delete/$', 'delete'),
)