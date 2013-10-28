from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from gestorpsi.authentication.forms import RegistrationForm
from gestorpsi.authentication.models import Profile
from gestorpsi.frontend.views import start as frontend_start
from django.contrib.auth.decorators import login_required
from gestorpsi.authentication.views import gestorpsi_login

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('gestorpsi.gcm.urls')),
    url(r'^accounts/register/$', 'gestorpsi.authentication.views.register', {'form_class': RegistrationForm }, name='registration_register'),
    url(r'^accounts/login/$', 'gestorpsi.authentication.views.gestorpsi_login', {'template_name': 'registration/login.html'}, name='auth_login'),
    (r'^accounts/', include('gestorpsi.authentication.urls')),
    (r'^accounts/', include('registration.urls')),
    (r'^$', login_required(frontend_start)),
    (r'^admin/', include(admin.site.urls)),
    (r'^contact/', include('gestorpsi.contact.urls')),
    (r'^place/', include('gestorpsi.place.urls')),
    (r'^careprofessional/', include('gestorpsi.careprofessional.urls')),
    (r'^client/', include('gestorpsi.client.urls')),
    (r'^client/', include('gestorpsi.demographic.urls')),
    (r'^client/', include('gestorpsi.ehr.urls')),
    #(r'^client/', include('gestorpsi.socioeconomic.urls')),
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
    (r'^report/', include('gestorpsi.report.urls')),
    (r'^support/', include('gestorpsi.support.urls')),
    (r'^frontend/', include('gestorpsi.frontend.urls')),
    (r'^profile/', include('gestorpsi.profile.urls')),
    (r'^util/', include('gestorpsi.util.urls')),
    (r'^chaining/', include('smart_selects.urls')),
    
    (r'^sentry/', include('sentry.web.urls')),

    (r'^payments/', include('gestorpsi.payments.urls')),
    
)



if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )

try:
    from gestorpsi.urls_local import *
except:
    pass




