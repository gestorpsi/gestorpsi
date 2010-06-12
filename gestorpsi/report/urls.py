# -*- coding: utf-8 -*-

"""
Copyright (C) 2008 GestorPsi

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

from django.conf.urls.defaults import *
from gestorpsi.report.views import *
from gestorpsi.report.forms import ReportSaveAdmissionForm
from gestorpsi.authentication.views import login_check

admission_save = {
    'form_class': ReportSaveAdmissionForm,
    'view': 'admission',
    'template': 'report/report_admission_save.html',
}

urlpatterns = patterns('',
    url(r'^$', login_check(index)),
    url(r'^date/$', login_check(report_date)),
    
    # statistics views
    url(r'^admission/$', login_check(admission_data)),
    url(r'^admission/demographic/$', login_check(demographic_data), {'view':'admission'}),
    url(r'^admission/chart/$', login_check(chart), {'view':'admission'}),

    ## list of clients
    url(r'^admission/client/overview/individuals/$', login_check(admission_client_report), {'view':'overview', 'filter':'individuals'}, name='admission_client_overview_individuals'),
    url(r'^admission/client/overview/companies/$', login_check(admission_client_report), {'view':'overview', 'filter':'companies', }, name='admission_client_overview_companies'),
    url(r'^admission/client/overview/total/$', login_check(admission_client_report), {'view':'overview', 'filter':'total'}, name='admission_client_overview_total'),
    url(r'^admission/client/signed/signed/$', login_check(admission_client_report), {'view':'signed', 'filter':'signed'}, name='admission_client_signed_signed'),
    url(r'^admission/client/signed/notsigned/$', login_check(admission_client_report), {'view':'signed', 'filter':'notsigned'}, name='admission_client_signed_notsigned'),
    url(r'^admission/client/knowledge/(?P<filter>[0-9]*)/$', login_check(admission_client_report), {'view':'knowledge', }, name='admission_client_knowledge'),

    # admission export
    url(r'^admission/export/$', login_check(admission_export), name='report_admission_export'),

    # save and saved reports
    url(r'^admission/save/$', login_check(report_save), admission_save),
    url(r'^saved/$', login_check(reports_saved)),
    url(r'^del/(?P<object_id>[0-9]*)/$', login_check(report_del), name='report_del'),
    url(r'^undelete/(?P<object_id>[0-9]*)/$', login_check(report_del), { 'undelete':True }, name='report_undelete'),
    url(r'^empty/$', login_check(report_empty), name='report_empty'),
    #url(r'^admission/load/(?P<object_id>[0-9]*)/$', login_check(report_load), {'view':'admission'}, name='report_load_admission'),
)
