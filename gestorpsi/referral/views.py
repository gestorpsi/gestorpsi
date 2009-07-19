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
from gestorpsi.referral.models import Referral
from gestorpsi.referral.forms import ReferralForm
from gestorpsi.util.decorators import permission_required_with_403

# add or edit form
@permission_required_with_403('referral.referral_read')
def form(request, object_id=''):
    try:
        object    = get_object_or_404(Client, pk=object_id)
    except:
        object = Client()
        
    # client referral
    data = {'client': [object.id]}
    referral_form = ReferralForm(data)
    referral_form.fields['referral'].queryset = Referral.objects.filter(client=object)
    referral_form.fields['service'].queryset = Service.objects.filter(active=True, organization=request.user.get_profile().org_active)
    #referral_form.fields['professional'].queryset = CareProfessional.objects.filter(person__organization = request.user.get_profile().org_active.id)
    referral_form.fields['client'].queryset = Client.objects.filter(person__organization = request.user.get_profile().org_active.id, clientStatus = '1')
    total_service = Referral.objects.filter(client=object).count()
    referral_list = Referral.objects.filter(client=object, status='01')
    
    return render_to_response('referral/referral_form.html',
                              {'object': object, 
                                'referral_form': referral_form,
                                'referral_list': referral_list,
                                'referrals': Referral.objects.filter(client = object),
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
    referral = Referral.objects.filter(client=object)
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

        array[i] = {
            'id': o.id,
            'status': o.status,
            'service': o.service.name,
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


""" *** TODO: manage multiples referrals """
@permission_required_with_403('referral.referral_write')
def save(request, object_id = None):
    if request.method == 'POST':
        form = ReferralForm(request.POST)
        if form.is_valid():
            object = form.save(commit=False)
            object.organization = request.user.get_profile().org_active
            object.status = '01'
            object.save()
            form.save_m2m()

    request.user.message_set.create(message=_('Referral saved successfully'))

    return HttpResponseRedirect('/client/%s/home' % request.POST.get('client_id'))
