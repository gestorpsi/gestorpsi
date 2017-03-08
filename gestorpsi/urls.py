# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
#from gestorpsi.authentication.forms import RegistrationForm
from gestorpsi.authentication.models import Profile
from gestorpsi.frontend.views import start as frontend_start
from django.contrib.auth.decorators import login_required
from gestorpsi.authentication.views import gestorpsi_login

from gestorpsi.settings import MEDIA_ROOT
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
    # url
    (r'^$', login_required(frontend_start)),
    url(r'^accounts/login/$', 'gestorpsi.authentication.views.gestorpsi_login', {'template_name': 'registration/login.html'}, name='auth_login'),

    # registration org form
    url(r'^accounts/register/$', 'gestorpsi.authentication.views.register', name='registration-register'),
    url(r'^accounts/complete/$', 'gestorpsi.authentication.views.complete', name='registration-complete'),

    # user custom admin for GCM
    url(r'^admin/gcm/$', 'gestorpsi.gcm.views.views.org_object_list', name='gcm-index'),

    # include
    (r'^accounts/', include('gestorpsi.authentication.urls')),
    (r'^accounts/', include('registration.urls')), # logout
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
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT, 'show_indexes': False}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT, 'show_indexes': False}),
    (r'^profile/', include('gestorpsi.profile.urls')),
    (r'^util/', include('gestorpsi.util.urls')),
    # (r'^chaining/', include('smart_selects.urls')),
    (r'^sentry/', include('sentry.web.urls')),
    (r'^gcm/', include('gestorpsi.gcm.urls')),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
