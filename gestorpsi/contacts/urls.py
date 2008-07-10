from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    #(r'^gestorpsi/', include('gestorpsi.foo.urls')),
    (r'^$', 'gestorpsi.contacts.views.index'),
    (r'^add/$', 'gestorpsi.contacts.views.add'),    
    (r'^(?P<pID>\d+)/$', 'gestorpsi.contacts.views.details'),
    (r'^delete/(?P<pID>\d+)/$', 'gestorpsi.contacts.views.delete'),
)


