from django.conf.urls.defaults import *
from django.contrib import admin
#from django.contrib.auth.views import login, logout

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^gestor/', include('gestor.foo.urls')),
    (r'^login/', include('gestorpsi.authentication.urls')),
        
    # Uncomment this for admin:
    #(r'^demo/', include('django.contrib.admin.urls')),
    (r'^$', 'gestorpsi.frontend.views.index'),    
    (r'^admin/(.*)', admin.site.root),
    # OLD: (r'^admin/', include('django.contrib.admin.urls')),    
    (r'^contact/', include('gestorpsi.contact.urls')),
    (r'^place/', include('gestorpsi.place.urls')),
    (r'^careprofessional/', include('gestorpsi.careprofessional.urls')),
    (r'^psychologist/', include('gestorpsi.psychologist.urls')),
    (r'^client/', include('gestorpsi.client.urls')),
    (r'^employee/', include('gestorpsi.employee.urls')),
    (r'^person/', include('gestorpsi.person.urls')),
    (r'^address/', include('gestorpsi.address.urls')),
    (r'^service/', include('gestorpsi.service.urls')),
    (r'^device/', include('gestorpsi.device.urls')),
    (r'^organization/', include('gestorpsi.organization.urls')),
    (r'^upload/', include('gestorpsi.upload.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media/', 'show_indexes': True}),
)