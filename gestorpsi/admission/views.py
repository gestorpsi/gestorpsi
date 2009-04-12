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
from gestorpsi.client.models import Client, PersonLink, Relation, IdRecordSeq
from gestorpsi.organization.models import Organization
from gestorpsi.careprofessional.models import LicenceBoard, CareProfessional
from gestorpsi.careprofessional.views import PROFESSIONAL_AREAS
from gestorpsi.admission.models import *
from gestorpsi.contact.views import *
from gestorpsi.util.views import date_form_to_db

def form(request, object_id=''):
    object = get_object_or_404(Client, pk=object_id)

    return render_to_response('admission/admission_form.html', {
        'address_book_professionals': address_book_get_professionals(request),
        'address_book_organizations': address_book_get_organizations(request),
        'object': object,
        'PROFESSIONAL_AREAS': PROFESSIONAL_AREAS,
        'licenceBoardTypes': LicenceBoard.objects.all(),
        'ReferralChoices': ReferralChoice.objects.all(),
        'IndicationsChoices': IndicationChoice.objects.all(),
        'Relations': Relation.objects.all(),
        'IdRecord': get_object_or_404(IdRecordSeq, uid=object_id),
    })

def is_responsible(value):
    if (value == 'on'):
        return True
    else:
        return False

def add_relationship(object, name_list, relation_list, responsible_list):
    responsible = ''
    object.person_link.all().delete()
    for i in range(0, len(name_list)):
        if (len(name_list[i])):
            try:
                responsible = is_responsible(responsible_list[i])
            except:
                responsible = False
            object.person_link.add(PersonLink.objects.create(person=Person.objects.create(name=name_list[i]), relation=Relation.objects.get(pk=relation_list[i]), responsible=responsible))

def save(request, object_id=''):
    object = get_object_or_404(Client, pk=object_id)
    object.admission_date = date_form_to_db(request.POST['admission_date'])
    object.legacyRecord = request.POST['legacyRecord']
    object.healthDocument = request.POST['healthDocument']
    object.comments = request.POST['comments']
    
    """ Referral Section """
    ar = AdmissionReferral()
    ar.referral_choice = ReferralChoice.objects.get(pk=request.POST['referral'])
    try:
        ar.referral_organization = Organization.objects.get(pk=request.POST['referral_organization'])
    except:
        ar.referral_organization = None
    try:
        ar.referral_professional = CareProfessional.objects.get(pk=request.POST['referral_professional'])
    except:
        ar.referral_professional = None
    ar.save()
    object.referral_choice = ar

    """ Indication  Section """
    indication = Indication()
    indication.indication_choice = IndicationChoice.objects.get(pk=request.POST['indication'])
    try:
        indication.referral_organization = Organization.objects.get(pk=request.POST['indication_organization'])
    except:
        indication.referral_organization = None
    try:
        indication.referral_professional = CareProfessional.objects.get(pk=request.POST['indication_professional'])
    except:
        indication.referral_professional = None
    indication.save()
    object.indication_choice = indication

    object.save()
    
    add_relationship(object, request.POST.getlist('parent_name'),request.POST.getlist('parent_relation'), request.POST.getlist('parent_responsible'))
    return HttpResponse(object.id)
