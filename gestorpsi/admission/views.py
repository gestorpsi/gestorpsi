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

from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from gestorpsi.client.models import Client, PersonLink, Relation
from gestorpsi.organization.models import Organization
from gestorpsi.careprofessional.models import LicenceBoard, CareProfessional
from gestorpsi.careprofessional.views import Profession
from gestorpsi.admission.models import *
from gestorpsi.contact.views import *
from gestorpsi.util.views import get_object_or_None
from gestorpsi.util.decorators import permission_required_with_403

## !! moved to client views
#def form(request, object_id=''):
    #object = get_object_or_404(Client, pk=object_id)

    #return render_to_response('admission/admission_form.html', {
        #'address_book_professionals': address_book_get_professionals(request),
        #'address_book_organizations': address_book_get_organizations(request),
        #'object': object,
        #'PROFESSIONAL_AREAS': PROFESSIONAL_AREAS,
        #'licenceBoardTypes': LicenceBoard.objects.all(),
        #'ReferralChoices': ReferralChoice.objects.all(),
        #'IndicationsChoices': IndicationChoice.objects.all(),
        #'Relations': Relation.objects.all(),
        ##'IdRecord': get_object_or_404(IdRecordSeq, uid=object_id),
    #})

@permission_required_with_403('admission.admission_read')
def is_responsible(value):
    if (value == 'on'):
        return True
    else:
        return False

@permission_required_with_403('admission.admission_write')
def add_relationship(request, object, name_list, relation_list, responsible_list):
    responsible = ''
    object.person_link.all().delete()
    for i in range(0, len(name_list)):
        if (len(name_list[i])):
            try:
                responsible = is_responsible(responsible_list[i])
            except:
                responsible = False
            object.person_link.add(PersonLink.objects.create(person=Person.objects.create(name=name_list[i]), relation=Relation.objects.get(pk=relation_list[i]), responsible=responsible))

@permission_required_with_403('admission.admission_write')
def save(request, object_id=''):
    object = get_object_or_404(Client, pk=object_id)
    object.admission_date = datetime.strptime(request.POST.get('admission_date'), '%d/%m/%Y')
    object.legacyRecord = request.POST.get('legacyRecord')
    object.healthDocument = request.POST.get('healthDocument')
    object.comments = request.POST.get('comments')

    """ Referral Section """
    ar = AdmissionReferral()
    ar.referral_choice = ReferralChoice.objects.get(pk=request.POST.get('referral'))
    ar.referral_organization = get_object_or_None(Organization, id=request.POST.get('referral_organization'))
    ar.referral_professional = get_object_or_None(CareProfessional, id=request.POST.get('referral_professional'))
    ar.client = object
    ar.save()

    """ Indication  Section """
    indication = Indication()
    indication.indication_choice = IndicationChoice.objects.get(pk=request.POST.get('indication'))
    indication.referral_organization = get_object_or_None(Organization, id=request.POST.get('indication_organization'))
    indication.referral_professional = get_object_or_None(CareProfessional, id=request.POST.get('indication_professional'))
    indication.client = object
    indication.save()

    object.save()
    
    add_relationship(request, object, request.POST.getlist('parent_name'),request.POST.getlist('parent_relation'), request.POST.getlist('parent_responsible'))
    return HttpResponse(object.id)
