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

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import gettext as _
from gestorpsi.address.models import Country, State, AddressType
from gestorpsi.phone.models import PhoneType
from gestorpsi.internet.models import EmailType, IMNetwork
from gestorpsi.document.models import TypeDocument, Issuer
from gestorpsi.person.models import MaritalStatus
from gestorpsi.person.views import person_save
from gestorpsi.careprofessional.models import CareProfessional, Profession
from gestorpsi.organization.models import Agreement
from gestorpsi.place.models import Place, PlaceType
from gestorpsi.service.models import Service
from gestorpsi.psychologist.models import Psychologist
from gestorpsi.careprofessional.views import care_professional_fill

# person form
def form(request):
    try:
        object = request.user.get_profile()
    except:
        raise Http404
    
    countries = Country.objects.all()
    PhoneTypes = PhoneType.objects.all()
    AddressTypes = AddressType.objects.all()
    EmailTypes = EmailType.objects.all()
    IMNetworks = IMNetwork.objects.all() 
    TypeDocuments = TypeDocument.objects.all()
    Issuers = Issuer.objects.all()
    States = State.objects.all()
    MaritalStatusTypes = MaritalStatus.objects.all()
    
    return render_to_response('profile/profile_person.html', locals(), context_instance=RequestContext(request))

def form_careprofessional(request):
    documents = []
    workplaces = []
    agreements = []
    try:
        object = CareProfessional.objects.get(pk=request.user.get_profile().person.careprofessional.id)
        workplaces = object.professionalProfile.workplace.all()
        agreements = object.professionalProfile.agreement.all()
    except:
        raise Http404

    return render_to_response('profile/profile_careprofessional.html', {
                                    'object': object,
                                    'PROFESSIONAL_AREAS': Profession.objects.all(),
                                    'AgreementTypes': Agreement.objects.all(),
                                    'WorkPlacesTypes': Place.objects.filter(organization = request.user.get_profile().org_active.id),
                                    'workplaces': workplaces,
                                    'agreements': agreements,
                                    'ServiceTypes': Service.objects.filter( active=True, organization=request.user.get_profile().org_active ),
                                    'PlaceTypes': PlaceType.objects.all(),
                                    },
                              context_instance=RequestContext(request)
                              )

def save(request):
    if not request.method == 'POST':
        raise Http404  
    try:
        person = request.user.get_profile().person
        person_save(request, person)
    except:
        raise Http404

    request.user.message_set.create(message=_('Profile updated successfully'))
    return HttpResponseRedirect('/profile/')
    
def save_careprofessional(request):    
    try:
        object = Psychologist.objects.get(pk=request.user.get_profile().person.careprofessional.id)        
    except:
        raise Http404

    object = care_professional_fill(request, object, None)
    object.save()

    request.user.message_set.create(message=_('Professional profile saved successfully'))

    return HttpResponseRedirect('/profile/careprofessional/')
