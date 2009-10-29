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

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson
from django.template import RequestContext
from django.utils.translation import ugettext as _
from gestorpsi.client.models import Client
from gestorpsi.service.models import Service
from gestorpsi.referral.models import Referral, ReferralGroup, Queue, ReferralExternal, ReferralAttach
from gestorpsi.referral.forms import ReferralGroupForm, ReferralClientForm
from gestorpsi.util.decorators import permission_required_with_403


# list referral groups
@permission_required_with_403('referral.referral_list')
def group_list(request, object_id=None):
    object  = ReferralGroup.objects.filter(referral__service__id = object_id, referral__organization = request.user.get_profile().org_active)

    return render_to_response('service/service_group_list.html',
                              { 'object': object, 
                               'service': Service.objects.get(pk=object_id),
                              },
                              context_instance=RequestContext(request)
                              )

# referral group add form from selected SERVICE
@permission_required_with_403('referral.referral_write')
def group_add(request, object_id=None):
    object = get_object_or_404(Service, pk=object_id, organization = request.user.get_profile().org_active)

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
        client_form.fields['client'].queryset = Client.objects.filter(person__organization = request.user.get_profile().org_active.id, clientStatus = '1', referral__service = object).distinct()

    return render_to_response('service/service_group_form.html',
                              {'object': object, 
                                'form': form,
                                'client_form': client_form,
                                'hide_service_actions': True,
#                                'clients': Client.objects.filter(person__organization = request.user.get_profile().org_active.id, clientStatus = '1', referral__service = object).distinct(),
                                'clients': Referral.objects.filter(organization = request.user.get_profile().org_active, status = '01', service = object).distinct(),
                               },
                              context_instance=RequestContext(request)
                              )
                              
# referral group edit form from selected GROUP
@permission_required_with_403('referral.referral_write')
def group_form(request, object_id=None):
    object = get_object_or_404(ReferralGroup, pk=object_id, referral__service__organization=request.user.get_profile().org_active)

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


@permission_required_with_403('referral.referral_list')
def mult_select(request, object_id = None):
    print "M U L T"
    object = get_object_or_404(Service, pk=object_id, organization = request.user.get_profile().org_active)
#    object = get_object_or_404(Client, pk=object_id, person__organization=request.user.get_profile().org_active)
#    referral = Referral.objects.charged().filter(client=object, service__organization=request.user.get_profile().org_active)

    referrals = Referral.objects.filter(organization = request.user.get_profile().org_active, status = '01', service = object).distinct()

    array = {} #json
    i = 0

    for o in referrals:
        prof0 = ''
        prof1 = ''
        prof2 = ''

        try:
            prof0 = '%s' % o.professional.all()[0]
            prof0 = ('(%s' ' %s)' % (prof0.split(' ')[0], prof0.split(' ')[1][0]))

            prof1 = '%s' % o.professional.all()[1]
            prof1 = ('(%s' ' %s)' % (prof1.split(' ')[0], prof1.split(' ')[1][0]))

            prof2 = '%s' % o.professional.all()[2]
            prof2 = ('(%s' ' %s)' % (prof2.split(' ')[0], prof2.split(' ')[1][0]))

        except:
            pass

        array[i] = {
            'client': '%s' % o.client.all()[0],
            'id': '%s' % o.client.all()[0].id,
            'prof0': ' %s' % prof0,
            'prof1': ' %s' % prof1,
            'prof2': ' %s' % prof2,
        }
        i = i + 1

    array = simplejson.dumps(array, encoding = 'iso8859-1')

    return HttpResponse(array, mimetype='application/json')
    
def _referral_view(request, object_id = None, referral_id = None, template_name = 'client/client_referral_home.html'):
    user = request.user
    object = get_object_or_404(Client, pk = object_id, person__organization=request.user.get_profile().org_active)
    referral = get_object_or_404(Referral, pk=referral_id, service__organization=request.user.get_profile().org_active)
    organization = user.get_profile().org_active.id
    queues = Queue.objects.filter(referral=referral_id, client=object)
    referrals = ReferralExternal.objects.filter(referral=referral_id)

    discharged_list = object.referrals_discharged()
    if discharged_list.filter(pk = referral_id).count():
        referral_discharged = True
    else: 
        referral_discharged = False

    clss = request.GET.get("clss")
    dt = referral.date.strftime("%d-%m-%Y  %H:%M ")
    try:
        indication = Indication.objects.get(referral = referral_id)
    except:
        indication = None
    attachs = ReferralAttach.objects.filter(referral = referral_id)

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
    
def _referral_occurrences(request, object_id = None, referral_id = None, type = 'upcoming', template_name='client/client_referral_occurrences.html'):
    object = get_object_or_404(Client, pk = object_id, person__organization=request.user.get_profile().org_active)
    referral = get_object_or_404(Referral, pk=referral_id, service__organization=request.user.get_profile().org_active)
    occurrences = referral.past_occurrences() if type == 'past' else  referral.upcoming_occurrences()
    
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
