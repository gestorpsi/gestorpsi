from django.conf.urls.defaults import *

urlpatterns= patterns('gestorpsi.service.views',
    (r'^$', 'index'),
    (r'^add/(\d+)$', 'form'),
    (r'^save/(\d+)$', 'save'),
    (r'^delete/(\d+)$', 'delete'),
)