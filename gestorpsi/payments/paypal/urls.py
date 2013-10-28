from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    (r'^single', 'gestorpsi.payments.paypal.views.single_payment', {}, 'single_payment'),
    (r'^subscribe', 'gestorpsi.payments.paypal.views.recurring_payment', {}, 'recurring_payment'),
    
    (r'^answer/receive/protect', include('packages.paypal.standard.ipn.urls')),
)




