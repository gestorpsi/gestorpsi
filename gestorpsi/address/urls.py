from django.conf.urls.defaults import *

urlpatterns = patterns('gestorpsi.address.views',
    (r'^search/city/(?P<city_name>[^/]+)/$', 'search_city'), 
)