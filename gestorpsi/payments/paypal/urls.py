from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    (r'^test', 'gestorpsi.payments.paypal.views.view_that_asks_for_money', {}, 'view_that_asks_for_money'),
    (r'^answer/receive/protect', include('packages.paypal.standard.ipn.urls')),
)




