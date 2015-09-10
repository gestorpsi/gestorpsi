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

from django.db.models.query_utils import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson
from django.template import RequestContext
from django.utils.translation import ugettext as _
from swingtime.models import Occurrence
from datetime import datetime

from gestorpsi.client.models import Client
from gestorpsi.service.models import Service
from gestorpsi.referral.models import Referral, Queue, ReferralExternal, ReferralAttach, REFERRAL_ATTACH_TYPE
from gestorpsi.util.decorators import permission_required_with_403
from gestorpsi.financial.models import Receive

@permission_required_with_403('referral.referral_list')
def referral_off(request, object_id=None):
    object = get_object_or_404(Referral, pk=object_id, service__organization=request.user.get_profile().org_active)
    referral.status = '02'
    referral.save(force_update = True)
    return HttpResponse(referral.id)

@permission_required_with_403('referral.referral_list')
def client_referrals(request, object_id = None):
    object = get_object_or_404(Client, pk=object_id, person__organization=request.user.get_profile().org_active)
    referral = Referral.objects.charged().filter(client=object, service__organization=request.user.get_profile().org_active)

    array = {} #json
    i = 0
    
    for o in referral:
        priority = ("%s" % o.priority).decode('utf-8')
        impact = ("%s" % o.impact).decode('utf-8')
        service_name = u'%s' % o

        array[i] = {
            'id': o.id,
            'status': o.status,
            'service':  service_name,
            'professional': o.professional,
            'reason': o.referral_reason,
            'annotation': o.annotation,
            'available_time': o.available_time,
            'priority': priority,
            'impact': impact,
            'data': o.date.strftime("%d/%m/%Y %H:%M:%S")
        }

        sub_count = 0
        array[i]['professional'] = {}
        for p in o.professional.all():
            array[i]['professional'][sub_count] = ({'id':p.id, 'name': '%s %s' % (p.person.name, '' if not p.is_student else _(' - Student')),})
            sub_count = sub_count + 1
        
        i = i + 1
    
    array = simplejson.dumps(array, encoding = 'iso8859-1')
    
    return HttpResponse(array, mimetype='application/json')


def _referral_view(request, object_id = None, referral_id = None, template_name = 'client/client_referral_home.html', access_check_referral_write = None):
    clss = request.GET.get("clss")
    user = request.user
    object = get_object_or_404(Client, pk = object_id, person__organization=request.user.get_profile().org_active)
    referral = get_object_or_404(Referral, pk=referral_id, service__organization=request.user.get_profile().org_active)
    organization = user.get_profile().org_active.id
    queues = Queue.objects.filter(referral=referral_id, client=object)
    referrals = ReferralExternal.objects.filter(referral=referral_id)
    payments = Receive.objects.filter(occurrence__event__referral=referral)

    '''
        avoid duplicate payment when is package
    '''
    tmpp = [] # past
    tmpu = [] # upcoming

    for x in Receive.objects.filter( Q(occurrence__event__referral=referral) | Q(referral=referral) ).order_by('-occurrence__start_time','-id').distinct():

        # past
        if x.get_is_conclude_(): 
            if not x in tmpp:
                tmpp.append(x)
        # upcoming
        else:
            if not x in tmpu:
                tmpu.append(x)

    receive_upcoming_small = tmpu[0:5]
    receive_upcoming_all = tmpu[5:]
    receive_past_small = tmpp[0:5]
    receive_past_all = tmpp[5:]


    try:
        discharged = ReferralDischarge.objects.get(referral=referral)
    except:
        pass

    try:
        indication = Indication.objects.get(referral = referral_id)
    except:
        indication = None

    attachs = ReferralAttach.objects.filter(referral = referral_id)

    # permission to read file, user can be is a professional and/or a psychologist.
    is_professional = user.get_profile().person.is_careprofessional()
    is_psychologist = False

    if is_professional:
        if str(user.get_profile().person.careprofessional.professionalIdentification.profession) == "Psicólogo":
            is_psychologist = True

    types = REFERRAL_ATTACH_TYPE

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
    

def _referral_occurrences(request, object_id=None, referral_id=None, type='upcoming', template_name='client/client_referral_occurrences.html'):

    object = get_object_or_404(Client, pk = object_id, person__organization=request.user.get_profile().org_active)
    referral = get_object_or_404(Referral, pk=referral_id, service__organization=request.user.get_profile().org_active)
    occurrences = referral.past_occurrences_all() if type=='past' else  referral.upcoming_occurrences()
    
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
