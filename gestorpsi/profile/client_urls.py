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
from gestorpsi.profile.client_views import *
from gestorpsi.authentication.views import login_check

urlpatterns = patterns('',
    url(r'^referral/$', login_check(referral_list), name='profile-client-referral-list'),
    url(r'^referral/(?P<object_id>\d+)/$', login_check(referral_home), name='profile-client-referral-home'),
    url(r'^referral/(?P<referral_id>\d+)/(?P<type>upcoming)/$', login_check(referral_occurrences)), # upcoming occurences
    url(r'^referral/(?P<referral_id>\d+)/(?P<type>past)/$', login_check(referral_occurrences)), # past occurences
    url(r'^referral/(?P<referral_id>\d+)/messages/$', login_check(referral_messages)), # referral messages
    url(r'^messages/chat/(?P<object_id>\d+)/$', login_check(occurrence_chat), name='profile-client-occurrence-chat'),
    url(r'^messages/chat/update/(?P<messagetopic_id>\d+)/(?P<lastmessage_id>\d+)/$', login_check(update_chat_message)),
    url(r'^messages/chat/exit/(?P<messagetopic_id>\d+)/$', login_check(exit_chat)),
    url(r'^messages/chat/postmessage/(?P<messagetopic_id>\d+)/$', login_check(chat_message)),
    url(r'^referral/(?P<referral_id>\d+)/messages/topic/(?P<topic_id>\d+)/newmessage$', login_check(new_topic_message)),
    url(r'^referral/(?P<referral_id>\d+)/messages/chat/(?P<scheduleoccurrence_id>\d+)$', login_check(chat_messages_history)), # referral topic messages
    url(r'^referral/(?P<referral_id>\d+)/messages/topic/(?P<topic_id>\d+)$', login_check(topic_messages)), # referral topic messages
)
