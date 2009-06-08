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

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson
from gestorpsi.client.models import Client
from gestorpsi.service.models import Service
from gestorpsi.careprofessional.models import CareProfessional
from gestorpsi.referral.models import Referral
from gestorpsi.referral.forms import ReferralForm
from gestorpsi.util.decorators import permission_required_with_403

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
        array[i] = {
            'id': o.id,
            'status': o.status,
            'service': o.service.name
        }

        sub_count = 0
        array[i]['professional'] = {}
        for p in o.professional.all():
            array[i]['professional'][sub_count] = ({'id':p.id, 'name':p.person.name})
            sub_count = sub_count + 1
        
        i = i + 1
    
    array = simplejson.dumps(array, encoding = 'iso8859-1')
    
    return HttpResponse(array)
    #return HttpResponse(array, mimetype='application/json')


""" *** TODO: manage multiples referrals """
@permission_required_with_403('referral.referral_write')
def save(request, object_id = None):
    if request.method == 'POST':
        form = ReferralForm(request.POST)
        #form = ReferralForm(request.POST, instance=object)
        if form.is_valid():
            object = form.save(commit=False)
            object.organization = request.user.get_profile().org_active
            object.status = '01'
            object.save()
            form.save_m2m()

    return HttpResponse(object.id)
