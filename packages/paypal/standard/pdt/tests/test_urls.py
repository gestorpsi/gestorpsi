from django.conf.urls.defaults import *

urlpatterns = patterns('packages.paypal.standard.pdt.views',
    (r'^pdt/$', 'pdt'),
)
