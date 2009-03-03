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
from gestorpsi.client.models import Client
from gestorpsi.service.models import Service
from gestorpsi.careprofessional.models import CareProfessional
from gestorpsi.referral.models import Referral

def form(request, object_id=''):
    user = request.user
    object = get_object_or_404(Client, pk=object_id)

    return render_to_response('referral/referral_form.html', {
        'object': object,
        'Professionals': CareProfessional.objects.filter(person__organization = user.get_profile().org_active.id),
        'Services': Service.objects.filter( active=True, organization=user.get_profile().org_active ),
    })

""" *** TODO: manage multiples referrals """
def save(request, object_id=''):
    object = get_object_or_404(Client, pk=object_id)

    referral = Referral()
    referral.client = object

    try:
        referral.service = Service.objects.get(pk=request.POST['service'])
    except:
        referral.service = None

    try:
        referral.professional = CareProfessional.objects.get(pk=request.POST['professional'])
    except:
        referral.professional = None

    referral.save()

    return HttpResponse(object.id)
