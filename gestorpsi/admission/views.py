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
from gestorpsi.client.models import Client, PersonLink, Relation
from gestorpsi.careprofessional.models import LicenceBoard
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
    })

def is_responsible(value):
    if (value == 'on'):
        return True
    else:
        return False

def add_relationship(object, name_list, relation_list, responsible_list):
    responsible = ''
    object.person_link.clear()
    for i in range(0, len(name_list)):
        if (len(name_list[i])):
            try:
                responsible = is_responsible(responsible_list[i])
            except:
                responsible = False
            object.person_link.add(PersonLink.objects.create(person=Person.objects.create(name=name_list[i]), relation=Relation.objects.get(pk=relation_list[i]), responsible=responsible))

    # Deletar
    #for relation in relation_list:
    #    person_link = PersonLink()
    #    person_link.person = Person.objects.create(name=relation[0])
    #    person_link.relation = Relation.objects.get(pk=relation[1])
    #    person_link.responsible = relation[2]
    #    person_link.save()
    #    object.person_link.add(person_link)

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