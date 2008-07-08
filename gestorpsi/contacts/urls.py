from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    #(r'^gestorpsi/', include('gestorpsi.foo.urls')),
    (r'^contacts/$', 'gestorpsi.contacts.views.index'),
    (r'^contacts/add/$', 'gestorpsi.contacts.views.add'),    
    (r'^contacts/(?P<pID>\d+)/$', 'gestorpsi.contacts.views.details'),
    (r'^contacts/delete/(?P<pID>\d+)/$', 'gestorpsi.contacts.views.delete'),
)


