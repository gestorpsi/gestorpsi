from django.conf.urls.defaults import *

urlpatterns = patterns('gestorpsi.address.views',
    (r'^search/city/(?P<city_name>[^/]+)/$', 'search_city'),
    #(r'^select/city/(?P<city_id>\d+)/$', 'select_city'),
    #(r'^select/state/(?P<city_id>\d+)/$', 'select_state'),
    #(r'^select/country/(?P<city_id>\d+)/$', 'select_country'),
)