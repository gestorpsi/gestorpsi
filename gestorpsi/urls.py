from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^gestor/', include('gestor.foo.urls')),

    # Uncomment this for admin:
    #(r'^demo/', include('django.contrib.admin.urls')),
    (r'^$', 'gestorpsi.frontend.views.index'),
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^contacts/', include('gestorpsi.contacts.urls')),
    (r'^places/', include('gestorpsi.places.urls')),
    (r'^client/', include('gestorpsi.client.urls')),
    
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media/', 'show_indexes': True}),
)
