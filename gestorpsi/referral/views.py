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
from gestorpsi.careprofessional.models import CareProfessional
from gestorpsi.service.models import Service
from gestorpsi.util.views import date_form_to_db

def form(request, object_id=''):
    user = request.user
#    object = get_object_or_404(Client, pk=object_id)

    return render_to_response('referral/referral_form.html', {
        'Professionals': CareProfessional.objects.filter(person__organization = user.org_active.id),
        'Services': Service.objects.filter( active=True, organization=user.org_active ),
    })


def save(request, object_id=''):
    object = get_object_or_404(Client, pk=object_id)
    object.admission_date = date_form_to_db(request.POST['admission_date'])
    object.idRecord = request.POST['idRecord']
    object.legacyRecord = request.POST['legacyRecord']
    object.healthDocument = request.POST['healthDocument']
    object.comments = request.POST['comments']
    object.save()
    add_relationship(object, request.POST.getlist('parent_name'),request.POST.getlist('parent_relation'), request.POST.getlist('parent_responsible'))
    return HttpResponse(object.id)