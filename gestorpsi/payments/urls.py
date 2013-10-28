from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    (r'^paypal/', include('gestorpsi.payments.paypal.urls')),
)




