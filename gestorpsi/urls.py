# -*- coding: utf-8 -*-

from django.conf.urls.defaults import url, patterns, include
from django.conf import settings
from django.contrib import admin
from gestorpsi.frontend.views import start as frontend_start
from django.contrib.auth.decorators import login_required

from gestorpsi.settings import MEDIA_ROOT, STATIC_ROOT

admin.autodiscover()

urlpatterns = patterns('',
    # url
    (r'^$', login_required(frontend_start)),

    # registration org form
    url(r'^accounts/login/$', 'gestorpsi.authentication.views.gestorpsi_login', {'template_name': 'authentication/authentication_login_form.html'}, name='accounts-login-form'),
    url(r'^accounts/register/$', 'gestorpsi.authentication.views.register', name='registration-register'),
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
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_ROOT, 'show_indexes': False}),
    (r'^profile/', include('gestorpsi.profile.urls')),
    (r'^util/', include('gestorpsi.util.urls')),
    # (r'^chaining/', include('smart_selects.urls')),
    (r'^sentry/', include('sentry.web.urls')),
    (r'^gcm/', include('gestorpsi.gcm.urls')),
    (r'^covenant/', include('gestorpsi.covenant.urls')),
    (r'^financial/', include('gestorpsi.financial.urls')),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )
