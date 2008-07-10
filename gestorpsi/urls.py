from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^gestor/', include('gestor.foo.urls')),

    # Uncomment this for admin:
    #(r'^demo/', include('django.contrib.admin.urls')),
    (r'^$', 'gestorpsi.frontend.views.index'),
    (r'^contacts/', include('gestorpsi.contacts.urls')),
    (r'^admin/', include('django.contrib.admin.urls')),
    
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media/', 'show_indexes': True}),
)
