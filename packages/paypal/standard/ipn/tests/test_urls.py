from django.conf.urls.defaults import *

urlpatterns = patterns('packages.paypal.standard.ipn.views',
    (r'^ipn/$', 'ipn'),
)
