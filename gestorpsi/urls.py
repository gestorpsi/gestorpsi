from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^gestor/', include('gestor.foo.urls')),

    # Uncomment this for admin:
    #(r'^demo/', include('django.contrib.admin.urls')),
     (r'^gestorpsi/', include('gestorpsi.contacts.urls')),
     (r'^admin/', include('django.contrib.admin.urls')),
)
