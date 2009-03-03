from django.conf.urls.defaults import *
from django.contrib import admin
from gestorpsi.authentication.forms import RegistrationForm
#from django.contrib.auth.views import login, logout
from django.contrib.auth.decorators import login_required
from gestorpsi.frontend.views import index as frontend_index

from gestorpsi.authentication.models import Profile

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^gestor/', include('gestor.foo.urls')),
    #url(r'^accounts/register/$', 'registration.views.register', {'form_class': RegistrationForm}),
    url(r'^accounts/register/$', 'registration.views.register', {'form_class': RegistrationForm, 'profile_callback':Profile.objects.create }, name='registration_register'),
    (r'^accounts/', include('gestorpsi.authentication.urls')),
    (r'^accounts/', include('registration.urls')),
    
        
    # Uncomment this for admin:
    #(r'^demo/', include('django.contrib.admin.urls')),
    (r'^$', login_required(frontend_index)),    
    (r'^admin/(.*)', admin.site.root),
    # OLD: (r'^admin/', include('django.contrib.admin.urls')),    
    (r'^contact/', include('gestorpsi.contact.urls')),
    (r'^place/', include('gestorpsi.place.urls')),
    (r'^careprofessional/', include('gestorpsi.careprofessional.urls')),
    (r'^psychologist/', include('gestorpsi.psychologist.urls')),
    (r'^client/', include('gestorpsi.client.urls')),
    (r'^admission/', include('gestorpsi.admission.urls')),
    (r'^referral/', include('gestorpsi.referral.urls')),
    (r'^employee/', include('gestorpsi.employee.urls')),
    (r'^person/', include('gestorpsi.person.urls')),
    (r'^address/', include('gestorpsi.address.urls')),
    (r'^service/', include('gestorpsi.service.urls')),
    (r'^device/', include('gestorpsi.device.urls')),
    (r'^organization/', include('gestorpsi.organization.urls')),
    (r'^upload/', include('gestorpsi.upload.urls')),
    (r'^schedule/', include('gestorpsi.schedule.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media/', 'show_indexes': False}),
)
