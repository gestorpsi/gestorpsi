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

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson
from django.template import RequestContext
from django.utils.translation import ugettext as _
from gestorpsi.client.models import Client
from gestorpsi.service.models import Service
from gestorpsi.referral.models import Referral, ReferralGroup
from gestorpsi.referral.forms import ReferralForm, ReferralGroupForm, ReferralClientForm
from gestorpsi.util.decorators import permission_required_with_403


# list referral groups
@permission_required_with_403('referral.referral_list')
def group_list(request, object_id=''):
    try:
        object  = ReferralGroup.objects.filter(referral__service__id = object_id, referral__organization = request.user.get_profile().org_active)
    except:
        raise Http404

    return render_to_response('service/service_group_list.html',
                              { 'object': object, 
                               'service': Service.objects.get(pk=object_id),
                              },
                              context_instance=RequestContext(request)
                              )

# referral group add form from selected SERVICE
@permission_required_with_403('referral.referral_write')
def group_add(request, object_id=''):
    try:
        object  = Service.objects.get(pk = object_id, organization = request.user.get_profile().org_active)
    except:
        raise Http404

    if request.method == 'POST':
        form = ReferralGroupForm(request.POST)
        client_form = ReferralClientForm(request.POST)
        if form.is_valid() and client_form.is_valid():
            # create 'empty' referral
            referral = Referral()
            referral.service = object
            referral.organization = request.user.get_profile().org_active
            referral.save()
            
            # save group details
            object = form.save(commit=False)
            object.referral = referral
            object.save()
            
            # if exists, add clients on referral
            client_form = ReferralClientForm(request.POST, instance=referral)
            client_form.save()

            request.user.message_set.create(message=_('Group saved successfully'))
            return HttpResponseRedirect('/service/group/%s/form/' % object.id)

    else:
        form = ReferralGroupForm()
        client_form = ReferralClientForm()
        client_form.fields['client'].queryset = Client.objects.filter(person__organization = request.user.get_profile().org_active.id, clientStatus = '1')

    return render_to_response('service/service_group_form.html',
                              {'object': object, 
                                'form': form,
                                'client_form': client_form,
                                'hide_service_actions': True,
                               },
                              context_instance=RequestContext(request)
                              )
                              
# referral group edit form from selected GROUP
@permission_required_with_403('referral.referral_write')
def group_form(request, object_id=''):
    try:
        object  = ReferralGroup.objects.get(pk = object_id)
    except:
        raise Http404

    if request.method == 'POST':
        form = ReferralGroupForm(request.POST, instance=object)
        client_form = ReferralClientForm(request.POST, instance=object.referral)
        if form.is_valid() and client_form.is_valid():
            object = form.save(commit=False)
            object.save()
            client_form.save()

            request.user.message_set.create(message=_('Group saved successfully'))
            return HttpResponseRedirect('/service/group/%s/form/' % object.id)

    else:
        form = ReferralGroupForm(instance=object)
        client_form = ReferralClientForm(instance=object.referral)

    return render_to_response('service/service_group_form.html',
                              {'object': object, 
                                'form': form,
                                'client_form': client_form,
                                'hide_service_actions': True,
                               },
                              context_instance=RequestContext(request)
                              )

@permission_required_with_403('referral.referral_list')
def referral_off(request, object_id=""):
    referral = Referral.objects.get(pk = object_id)
    referral.status = '02'
    referral.save(force_update = True)
    return HttpResponse(referral.id)

@permission_required_with_403('referral.referral_list')
def client_referrals(request, object_id = None):
    object = get_object_or_404(Client, pk=object_id)
    referral = Referral.objects.charged().filter(client=object)

    array = {} #json
    i = 0
    
    for o in referral:

        if o.priority == None:
            priority = ""
        else:
            priority = ("%s" % o.priority).decode('utf-8')

        if o.impact == None:
            impact = ""
        else:
            impact = ("%s" % o.impact).decode('utf-8')
        try:
            service_name = o.service.name
        except:
            service_name = ''
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
            array[i]['professional'][sub_count] = ({'id':p.id, 'name':p.person.name})
            sub_count = sub_count + 1
        
        i = i + 1
    
    array = simplejson.dumps(array, encoding = 'iso8859-1')
    
    return HttpResponse(array, mimetype='application/json')

