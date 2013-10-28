from django.conf.urls.defaults import *

urlpatterns = patterns('packages.paypal.standard.ipn.views',            
    url(r'^$', 'ipn', name="paypal-ipn"),
)