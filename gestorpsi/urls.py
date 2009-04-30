from django.conf.urls.defaults import *
from django.contrib import admin
from gestorpsi.authentication.forms import RegistrationForm
from gestorpsi.authentication.models import Profile

from gestorpsi.frontend.views import index as frontend_index
from django.contrib.auth.decorators import login_required

#from gestorpsi.authentication.views import include_login_required

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^accounts/register/$', 'registration.views.register', {'form_class': RegistrationForm }, name='registration_register'),
    (r'^accounts/', include('gestorpsi.authentication.urls')),
    (r'^accounts/', include('registration.urls')),
    (r'^$', login_required(frontend_index)),    
    (r'^admin/(.*)', admin.site.root),
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
    (r'^user/', include('gestorpsi.users.urls')),
    (r'^schedule/', include('gestorpsi.schedule.urls')),
    (r'^frontend/', include('gestorpsi.frontend.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media/', 'show_indexes': False}),
)
