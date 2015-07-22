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
from gestorpsi.client.views import index, list, form, save, client_print, \
        organization_clients, add, home, order, referral_save, referral_list, referral_home, \
        referral_form, referral_discharge_form, schedule_daily, schedule_add, \
        occurrence_view, referral_occurrences, referral_plus_form, referral_plus_save, referral_queue, \
        referral_queue_save, referral_queue_remove, referral_ext_form, referral_ext_save, family, family_form, \
        add_company, company_related, company_related_form, referral_occurrences_action
from gestorpsi.online_messages.views import referral_messages, occurrence_chat, chat_message, update_chat_message, exit_chat, client_messages, new_message_topic, topic_messages, new_topic_message, chat_messages_history
from gestorpsi.authentication.views import login_check
from gestorpsi.organization.views import list_prof_org

urlpatterns = patterns('',

    # client list index and paginator 
    (r'^$', login_check(index)), #index
    (r'^list/$', login_check(list)), #list objects
    (r'^page(?P<page>(\d)+)$', login_check(list)), #list objects
    #(r'^initial/(?P<initial>[a-zA-Z])/page(?P<page>(\d)+)/$', login_check(list)), # quick filter
    url(r'^deactive/$', login_check(index), {'deactive': True} ), #list objects
    url(r'^list/deactive/$', login_check(list), {'deactive': True}), #list objects

    # client search person family, return JSON
    #(r'^filter/(?P<filter>\w+)/page(?P<page>(\d)+)/$', login_check(list), {'no_paging': True, 'retrn':'json'}), # quick search
    (r'^filter/(?P<filter>\w+)/$', login_check(list), {'no_paging': True, 'retrn':'json'}), # quick search

    (r'^add/$', login_check(add)), #new object form
    (r'^add/company/$', login_check(add_company)), #new object form
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/home/$', login_check(home)),
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/order/$', login_check(order)),
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', login_check(form)),

    (r'^save/$', login_check(save)), #save new object
    url(r'^save/company/$', login_check(save), {'is_company':True}), #save company client
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/company_clients/$', login_check(company_related)), # company related clients
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/company_clients/form/$', login_check(company_related_form)), # company related clients form
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/company_clients/(?P<company_client_id>\d+)/form/$', login_check(company_related_form)), # company related clients form
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/save/$', login_check(save)),  #update client
    url(r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/save/company/$', login_check(save), {'is_company':True}),  #update company client
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/print/$', login_required(client_print)),  # print record
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
    url(r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/referral/(?P<referral_id>\d+)/action/$', login_check(referral_occurrences_action), name="referral-occurrences-action"), # uncheck a event or lot.
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/referral/(?P<referral_id>\d+)/(?P<type>upcoming)/$', login_check(referral_occurrences)), # upcoming occurences
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/referral/(?P<referral_id>\d+)/(?P<type>past)/$', login_check(referral_occurrences)), # past occurences
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/referral/(?P<discharged>discharged)/$', login_check(referral_list)), # descharged referrals list
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/referral/(?P<referral_id>\d+)/$', login_check(referral_home)), # referral home
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/referral/(?P<referral_id>\d+)/discharge/$', login_check(referral_discharge_form)), # referral shutdown
    url(r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/referral/(?P<referral_id>\d+)/discharge/(?P<discharge_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/edit/$', login_check(referral_discharge_form), name='referral_discharge_edit'), # referral shutdown
#    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/occurence/(?P<occurrence_id>\d+)/confirmation/$', login_check(occurrence_confirmation)), # occurence confirmation
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/occurence/(?P<occurrence_id>\d+)/$', login_check(occurrence_view)), # occurence confirmation
    (r'^schedule/daily/$', login_check(schedule_daily)), # book client (schedule daily view)
    (r'^schedule/add/$', login_check(schedule_add)), # book client (schedule add form)

    url(r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/referral/(?P<referral_id>\d+)/messages/$', login_check(referral_messages)), # referral messages
    url(r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/referral/(?P<referral_id>\d+)/messages/newtopic$', login_check(new_message_topic), name='messages-newtopic'), # referral messages (new topic)
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/referral/(?P<referral_id>\d+)/messages/topic/(?P<topic_id>\d+)$', login_check(topic_messages)), # referral topic messages
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/referral/(?P<referral_id>\d+)/messages/topic/(?P<topic_id>\d+)/newmessage$', login_check(new_topic_message)), # referral topic messages
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/messages/chat/(?P<scheduleoccurrence_id>\d+)/$', login_check(occurrence_chat)), # event chat
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/referral/(?P<referral_id>\d+)/messages/chat/(?P<scheduleoccurrence_id>\d+)$', login_check(chat_messages_history)), # referral topic messages
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/messages/chat/postmessage/(?P<messagetopic_id>\d+)/$', login_check(chat_message)), # event chat
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/messages/chat/update/(?P<messagetopic_id>\d+)/(?P<lastmessage_id>\d+)/$', login_check(update_chat_message)), # event chat
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/messages/chat/exit/(?P<messagetopic_id>\d+)/$', login_check(exit_chat)), # exit chat
    #(r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/messages/$', login_check(client_messages)), # all messages for this client - inbox

    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/referral/(?P<referral_id>\d+)/queue/$', login_check(referral_queue)), # queue form
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/referral/(?P<referral_id>\d+)/queue/save/$', login_check(referral_queue_save)), # queue form save
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/referral/(?P<referral_id>\d+)/queue/(?P<queue_id>\d+)/remove/$', login_check(referral_queue_remove)), # queue form remove
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/family/$', login_check(family)), # client family
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/family/form/$', login_check(family_form)), # client family
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/family/(?P<relation_id>\d+)/form/$', login_check(family_form)), # client family
)
