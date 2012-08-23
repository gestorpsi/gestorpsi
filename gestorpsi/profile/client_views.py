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

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.utils.translation import gettext as _
from gestorpsi.client.models import Client
from gestorpsi.referral.models import Referral
from gestorpsi.schedule.models import Occurrence
from gestorpsi.online_messages.models import MessageTopic
from gestorpsi.referral.views import _referral_view
from gestorpsi.referral.views import _referral_occurrences
from gestorpsi.schedule.models import ScheduleOccurrence
from gestorpsi.online_messages.views import _occurrence_chat
from gestorpsi.online_messages.views import _update_chat_message
from gestorpsi.online_messages.views import _exit_chat
from gestorpsi.online_messages.views import _chat_message
from gestorpsi.online_messages.views import _topic_messages
from gestorpsi.online_messages.views import _chat_messages_history
from gestorpsi.online_messages.views import _referral_messages
from gestorpsi.online_messages.views import _new_topic_message


def referral_list(request):
    if not request.user.get_profile().person.is_client():
        raise Http404
    object = get_object_or_404(Client, pk=request.user.get_profile().person.client.id)

    return render_to_response('profile/client/referral_list.html', locals(), context_instance=RequestContext(request))

def referral_occurrences(request, referral_id = None, type = 'upcoming'):
    client = get_object_or_404(Client, pk=request.user.get_profile().person.client.id)
    if not request.user.get_profile().person.is_client() \
        or client not in [c for c in Referral.objects.get(pk=referral_id).client.all()]:
        raise Http404
    return _referral_occurrences(request, client.id, referral_id, type, 'profile/client/referral_occurrences.html')

def referral_home(request, object_id = None):
    client = get_object_or_404(Client, pk=request.user.get_profile().person.client.id)
    if not request.user.get_profile().person.is_client() \
        or client not in [c for c in Referral.objects.get(pk=object_id).client.all()]:
        raise Http404
    return _referral_view(request, client.id, object_id, 'profile/client/referral_home.html')

def referral_messages(request, referral_id):
    client = get_object_or_404(Client, pk=request.user.get_profile().person.client.id)
    if not request.user.get_profile().person.is_client() \
        or client not in [c for c in Referral.objects.get(pk=referral_id).client.all()]:
        raise Http404
    return _referral_messages(request, referral_id,  client.id, "profile/client/messages_referral.html")

def occurrence_chat(request, object_id = None):
    client = get_object_or_404(Client, pk=request.user.get_profile().person.client.id)
    if not request.user.get_profile().person.is_client() \
        or client not in [c for c in Occurrence.objects.get(pk=object_id).event.referral.client.all()]:
        raise Http404
    return _occurrence_chat(request, client.id, object_id, 'profile/client/messages_chat.html')

def update_chat_message(request, messagetopic_id, lastmessage_id):
    client = get_object_or_404(Client, pk=request.user.get_profile().person.client.id)
    if not request.user.get_profile().person.is_client() \
        or client not in [c for c in MessageTopic.objects.get(pk=messagetopic_id).referral.client.all()]:
        raise Http404
    return _update_chat_message(request, client.id, messagetopic_id, lastmessage_id)

def chat_message(request, messagetopic_id):
    client = get_object_or_404(Client, pk=request.user.get_profile().person.client.id)
    if not request.user.get_profile().person.is_client() \
        or client not in [c for c in MessageTopic.objects.get(pk=messagetopic_id).referral.client.all()]:
        raise Http404
    return _chat_message(request, client.id, messagetopic_id)

def chat_messages_history(request, scheduleoccurrence_id, referral_id):
    client = get_object_or_404(Client, pk=request.user.get_profile().person.client.id)
    scheduleoccurrence = ScheduleOccurrence.objects.get(pk=scheduleoccurrence_id)

    if scheduleoccurrence.messagetopic_set.count() > 0:
        messagetopic = scheduleoccurrence.messagetopic_set.all()[0]
    return _chat_messages_history(request, client.id, scheduleoccurrence_id, referral_id, "/profile/client/referral/%s/messages/topic/%s" % (referral_id, messagetopic.id))

def topic_messages(request, referral_id, topic_id):
    client = get_object_or_404(Client, pk=request.user.get_profile().person.client.id)
    if not request.user.get_profile().person.is_client() \
        or client not in [c for c in MessageTopic.objects.get(pk=topic_id).referral.client.all()]:
        raise Http404
    return _topic_messages(request, referral_id, topic_id, client.id, "profile/client/messages_topic.html")

def new_topic_message(request, referral_id, topic_id):
    client = get_object_or_404(Client, pk=request.user.get_profile().person.client.id)
    if not request.user.get_profile().person.is_client() \
        or client not in [c for c in Referral.objects.get(pk=referral_id).client.all()]:
        raise Http404
    return _new_topic_message(request, referral_id, topic_id, client.id, \
        '/profile/client/referral/%s/messages/topic/%s' % (referral_id, topic_id),
    )

def exit_chat(request, messagetopic_id):
    client = get_object_or_404(Client, pk=request.user.get_profile().person.client.id)
    if not request.user.get_profile().person.is_client() \
        or client not in [c for c in MessageTopic.objects.get(pk=messagetopic_id).referral.client.all()]:
        raise Http404
    return _exit_chat(request, client.id, messagetopic_id, '/profile/client/referral/%s' % MessageTopic.objects.get(pk=messagetopic_id).referral.id)
