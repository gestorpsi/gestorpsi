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
from django.contrib.auth.decorators import login_required
from gestorpsi.client.views import index, list, form, save, print_list, print_record, \
        organization_clients, add, home, order, referral_save, referral_list, referral_home, \
        referral_form, referral_discharge_form, schedule_daily, schedule_add, \
        occurrence_view, referral_occurrences, referral_plus_form, referral_plus_save, referral_queue, \
        referral_queue_save, referral_queue_remove, referral_ext_form, referral_ext_save, family
from gestorpsi.authentication.views import login_check
from gestorpsi.organization.views import list_prof_org

urlpatterns = patterns('',
    (r'^$', login_check(index)), #list objects
    (r'^page(?P<page>(\d)+)$', login_check(list)), #list objects
    (r'^initial/(?P<initial>[a-z])/page(?P<page>(\d)+)/$', login_check(list)), # quick filter
    (r'^filter/(?P<filter>.*)/page(?P<page>(\d)+)/$', login_check(list)), # quick search
    (r'^filter/(?P<filter>.*)/$', login_check(list), {'no_paging': True}), # quick search
    (r'^add/$', login_check(add)), #new object form
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/home/$', login_check(home)),
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/order/$', login_check(order)),
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', login_check(form)),

    (r'^save/$', login_check(save)), #save new object
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/save/$', login_check(save)),  #update object
#    (r'^(?P<object_id>\d+)/delete/$', login_check(delete)), # delete object
#    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/delete/$', login_check(delete)),  #delete object
    (r'^print/$', login_required(print_list)), # print client list
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/print/$', login_required(print_record)),  # print record
    (r'^organization_clients/$', login_required(organization_clients)),  # clients for logged otganization

    (r'^org/(?P<org_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/listprofessional/$', login_check(list_prof_org)), # get all professional of organization
    
    # referral
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/referral/ext/(?P<referral_id>\d+)/form/$', login_check(referral_ext_form)), # referral external form
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/referral/ext/(?P<referral_id>\d+)/save/$', login_check(referral_ext_save)), # referral external save

    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/referral/form/$', login_check(referral_form)), # add form
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/referral/plus/(?P<referral_id>\d+)/form/$', login_check(referral_plus_form)), # add form plus
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/referral/(?P<referral_id>\d+)/form/$', login_check(referral_form)), # edit form
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/referral/save/$', login_check(referral_save)), # referral add
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/referral/plus/save/$', login_check(referral_plus_save)), # referral add plus
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/referral/(?P<referral_id>\d+)/save/$', login_check(referral_save)), # referral save
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/referral/$', login_check(referral_list)), # charged referrals list
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/referral/(?P<referral_id>\d+)/(?P<type>upcoming)/$', login_check(referral_occurrences)), # upcoming occurences
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/referral/(?P<referral_id>\d+)/(?P<type>past)/$', login_check(referral_occurrences)), # past occurences
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/referral/(?P<discharged>discharged)/$', login_check(referral_list)), # descharged referrals list
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/referral/(?P<referral_id>\d+)/$', login_check(referral_home)), # referral home
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/referral/(?P<referral_id>\d+)/discharge/$', login_check(referral_discharge_form)), # referral shutdown
#    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/occurence/(?P<occurrence_id>\d+)/confirmation/$', login_check(occurrence_confirmation)), # occurence confirmation
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/occurence/(?P<occurrence_id>\d+)/$', login_check(occurrence_view)), # occurence confirmation
    (r'^schedule/daily/$', login_check(schedule_daily)), # book client (schedule daily view)
    (r'^schedule/add/$', login_check(schedule_add)), # book client (schedule add form)
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/referral/(?P<referral_id>\d+)/queue/$', login_check(referral_queue)), # queue form
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/referral/(?P<referral_id>\d+)/queue/save/$', login_check(referral_queue_save)), # queue form save
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/referral/(?P<referral_id>\d+)/queue/(?P<queue_id>\d+)/remove/$', login_check(referral_queue_remove)), # queue form remove
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/family/$', login_check(family)), # client family

    # DEACTIVES
    (r'^deactive/$', login_check(index), {'deactive': True} ), #list objects
    (r'^page(?P<page>(\d)+)/deactive/$', login_check(list), {'deactive':True} ), #list objects
    (r'^initial/(?P<initial>[a-z])/page(?P<page>(\d)+)/deactive/$', login_check(list), {'deactive': True}), # quick filter
    (r'^filt/(?P<filter>.*)/page(?P<page>(\d)+)/deactive/$', login_check(list), {'deactive': True}), # quick search
    (r'^filt/(?P<filter>.*)/deactive/$', login_check(list), {'no_paging': True, 'deactive': True}), # quick search
)
