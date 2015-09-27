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
from gestorpsi.report.forms import *
from gestorpsi.authentication.views import login_check
from gestorpsi.report.models import ReportAdmission, ReportReferral

# report urls save
admission_save = {
    'form_class': ReportSaveAdmissionForm,
    'view': 'admission',
}

referral_save = {
    'form_class': ReportSaveReferralForm,
    'view': 'referral',
}

receive_save = {
    'form_class': ReportSaveReceiveForm,
    'view': 'receive',
}

urlpatterns = patterns('',
    url(r'^$', login_check(index)),
    url(r'^date/$', login_check(report_date)),
    
    # statistics views
    url(r'^admission/$', login_check(admission_data), {'template':'report/report_table.html'}),
    url(r'^admission/demographic/$', login_check(demographic_data), {'view':'admission'}),
    #url(r'^admission/chart/$', login_check(chart), {'view':'admission'}),
    #url(r'^referral/chart/$', login_check(chart), {'view':'referral'}),
    url(r'^referral/$', login_check(referral_data), {'template':'report/report_table.html'}),
    url(r'^receive/$', login_check(receive_data) ),
    url(r'^event/$', login_check(event_data) ),

    ## list of clients from admissions
    url(r'^admission/client/overview/total/$', login_check(report_client_list), {'report_class': ReportAdmission, 'view':'overview', 'filter':'total'}, name='admission_client_overview_total'),
    url(r'^admission/client/overview/individuals/$', login_check(report_client_list), {'report_class': ReportAdmission, 'view':'overview', 'filter':'individuals'}, name='admission_client_overview_individuals'),
    url(r'^admission/client/overview/companies/$', login_check(report_client_list), {'report_class': ReportAdmission, 'view':'overview', 'filter':'companies', }, name='admission_client_overview_companies'),
    url(r'^admission/client/signed/signed/$', login_check(report_client_list), {'report_class': ReportAdmission, 'view':'signed', 'filter':'signed'}, name='admission_client_signed_signed'),
    url(r'^admission/client/signed/notsigned/$', login_check(report_client_list), {'report_class': ReportAdmission, 'view':'signed', 'filter':'notsigned'}, name='admission_client_signed_notsigned'),
    url(r'^admission/client/knowledge/(?P<filter>[0-9]*)/$', login_check(report_client_list), {'report_class': ReportAdmission, 'view':'knowledge', }, name='admission_client_knowledge'),

    ## list of clients from referral
    url(r'^referral/client/overview/total/$', login_check(report_client_list), {'report_class': ReportReferral, 'view':'overview', 'filter':'total'}, name='referral_client_overview_total'),
    url(r'^referral/client/overview/charged/$', login_check(report_client_list), {'report_class': ReportReferral, 'view':'overview', 'filter':'charged'}, name='referral_client_overview_charged'),
    url(r'^referral/client/overview/discharged/$', login_check(report_client_list), {'report_class': ReportReferral, 'view':'overview', 'filter':'discharged'}, name='referral_client_overview_discharged'),
    url(r'^referral/client/overview/discharged_discussed/$', login_check(report_client_list), {'report_class': ReportReferral, 'view':'overview', 'filter':'discharged_discussed'}, name='referral_client_overview_discharged_discussed'),
    url(r'^referral/client/overview/discharged_not_discussed/$', login_check(report_client_list), {'report_class': ReportReferral, 'view':'overview', 'filter':'discharged_not_discussed'}, name='referral_client_overview_discharged_not_discussed'),
    url(r'^referral/client/overview/internal/$', login_check(report_client_list), {'report_class': ReportReferral, 'view':'overview', 'filter':'internal'}, name='referral_client_overview_internal'),
    url(r'^referral/client/overview/external/$', login_check(report_client_list), {'report_class': ReportReferral, 'view':'overview', 'filter':'external'}, name='referral_client_overview_external'),
    url(r'^referral/client/knowledge/(?P<filter>[0-9]*)/$', login_check(report_client_list), {'report_class': ReportReferral, 'view':'knowledge', }, name='referral_client_knowledge'),    
    url(r'^referral/client/services/(?P<filter>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', login_check(report_client_list), {'report_class': ReportReferral, 'view':'services', }, name='referral_client_services'),
    url(r'^referral/client/knowledge/(?P<filter>[0-9]*)/$', login_check(report_client_list), {'report_class': ReportReferral, 'view':'knowledge', }, name='referral_client_knowledge'),    
    url(r'^referral/client/services/(?P<filter>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', login_check(report_client_list), {'report_class': ReportReferral, 'view':'services', }, name='referral_client_services'),
    url(r'^referral/client/internal/(?P<filter>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', login_check(report_client_list), {'report_class': ReportReferral, 'view':'internal', }, name='referral_client_internal'),
    url(r'^referral/client/internal_from/(?P<filter>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', login_check(report_client_list), {'report_class': ReportReferral, 'view':'internal_from', }, name='referral_client_internal_from'),
    url(r'^referral/client/external/(?P<filter>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', login_check(report_client_list), {'report_class': ReportReferral, 'view':'external', }, name='referral_client_external'),
    url(r'^referral/client/discharge/(?P<filter>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', login_check(report_client_list), {'report_class': ReportReferral, 'view':'discharge', }, name='referral_client_discharge'),
    url(r'^referral/client/discharge_reason/(?P<filter>[0-9]*)/$', login_check(report_client_list), {'report_class': ReportReferral, 'view':'discharge_reason', }, name='referral_client_discharge_reason'),
    url(r'^referral/client/discharge_discussed/(?P<filter>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', login_check(report_client_list), {'report_class': ReportReferral, 'view':'discharge_discussed', }, name='referral_client_discharge_discussed'),
    url(r'^referral/client/professional/(?P<filter>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', login_check(report_client_list), {'report_class': ReportReferral, 'view':'professional', }, name='referral_client_professional'),

    #url(r'^referral/client/overview/individuals/$', login_check(report_client_list), {'report_class': ReportReferral, 'view':'overview', 'filter':'individuals'}, name='admission_client_overview_individuals'),
    #url(r'^referral/client/overview/companies/$', login_check(report_client_list), {'report_class': ReportReferral, 'view':'overview', 'filter':'companies', }, name='admission_client_overview_companies'),
    #url(r'^referral/client/signed/signed/$', login_check(report_client_list), {'report_class': ReportReferral, 'view':'signed', 'filter':'signed'}, name='admission_client_signed_signed'),
    #url(r'^referral/client/signed/notsigned/$', login_check(report_client_list), {'report_class': ReportReferral, 'view':'signed', 'filter':'notsigned'}, name='admission_client_signed_notsigned'),

    # admission export
    #url(r'^admission/export/$', login_check(admission_export), name='report_admission_export'),
    url(r'^export/$', login_check(report_export), name='report_export'),

    # save and saved reports
    url(r'^receive/save/$', login_check(report_save), receive_save, name='report_receive_save'),
    url(r'^admission/save/$', login_check(report_save), admission_save, name='report_admission_save'),
    url(r'^referral/save/$', login_check(report_save), referral_save, name='report_referral_save'),
    url(r'^saved/$', login_check(reports_saved)),
    url(r'^del/(?P<object_id>[0-9]*)/$', login_check(report_del), name='report_del'),
    url(r'^undelete/(?P<object_id>[0-9]*)/$', login_check(report_del), { 'undelete':True }, name='report_undelete'),
    url(r'^empty/$', login_check(report_empty), name='report_empty'),
    #url(r'^admission/load/(?P<object_id>[0-9]*)/$', login_check(report_load), {'view':'admission'}, name='report_load_admission'),
)
