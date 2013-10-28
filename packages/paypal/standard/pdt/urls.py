from django.conf.urls.defaults import *

urlpatterns = patterns('packages.paypal.standard.pdt.views',
    url(r'^$', 'pdt', name="paypal-pdt"),
)