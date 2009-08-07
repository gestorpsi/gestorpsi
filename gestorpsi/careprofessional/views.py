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
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.utils.translation import ugettext as _
from gestorpsi.person.models import Person, MaritalStatus
from gestorpsi.person.views import person_json_list, person_save
from gestorpsi.careprofessional.models import ProfessionalProfile, ProfessionalIdentification, CareProfessional, Profession
from gestorpsi.organization.models import Agreement
from gestorpsi.phone.models import PhoneType
from gestorpsi.address.models import Country, State, AddressType, City
from gestorpsi.internet.models import EmailType, IMNetwork
from gestorpsi.document.models import TypeDocument, Issuer
from gestorpsi.place.models import Place, PlaceType
from gestorpsi.service.models import Service
from gestorpsi.util.decorators import permission_required_with_403
from gestorpsi.util.views import get_object_or_None


@permission_required_with_403('careprofessional.careprofessional_list')
def index(request):
    return render_to_response('careprofessional/careprofessional_list.html', context_instance=RequestContext(request))
  

@permission_required_with_403('careprofessional.careprofessional_list')
def list(request, page = 1):
    user = request.user
    object = CareProfessional.objects.filter(person__organization = user.get_profile().org_active.id).order_by('person__name')
    
    return HttpResponse(simplejson.dumps(person_json_list(request, object, 'careprofessional.careprofessional_read', page)),
                            mimetype='application/json')

@permission_required_with_403('careprofessional.careprofessional_read')
def form(request, object_id=''):
    user = request.user
    phones = []
    addresses = []
    emails    = []
    sites     = []
    instantMessengers = []
    documents = []
    workplaces = []
    agreements = []

    try:
        object = get_object_or_404(CareProfessional, pk=object_id)
        phones= object.person.phones.all()
        addresses= object.person.address.all()
        documents = object.person.document.all()                       
        emails    = object.person.emails.all()
        sites     = object.person.sites.all()
        instantMessengers = object.person.instantMessengers.all()
        workplaces = object.professionalProfile.workplace.all()
        agreements = object.professionalProfile.agreement.all()
    except:
        object = CareProfessional() 

    try:
        cities = City.objects.filter(state=request.user.get_profile().org_active.address.all()[0].city.state)
    except:
        cities = {}

    return render_to_response('careprofessional/careprofessional_form.html', {
                                    'object': object,
                                    'emails': emails,
                                    'websites': sites,
                                    'ims': instantMessengers,
                                    'addresses': addresses,
                                    'phones': phones,
                                    'documents': documents,
                                    'PROFESSIONAL_AREAS': Profession.objects.all(),
                                    'AgreementTypes': Agreement.objects.all(),
                                    'WorkPlacesTypes': Place.objects.filter(organization = user.get_profile().org_active.id),
                                    'countries': Country.objects.all(),
                                    'PhoneTypes': PhoneType.objects.all(),
                                    'AddressTypes': AddressType.objects.all(),
                                    'EmailTypes': EmailType.objects.all(),
                                    'IMNetworks': IMNetwork.objects.all() ,
                                    'TypeDocuments': TypeDocument.objects.all(),
                                    'Issuers': Issuer.objects.all(),
                                    'States': State.objects.all(),
                                    'MaritalStatusTypes': MaritalStatus.objects.all(),
                                    'PlaceTypes': PlaceType.objects.all(),
                                    'workplaces': workplaces,
                                    'agreements': agreements,
                                    'ServiceTypes': Service.objects.filter( active=True, organization=user.get_profile().org_active ),
                                    'Cities': cities,
                                    },
                              context_instance=RequestContext(request)
                              )

@permission_required_with_403('careprofessional.careprofessional_write')
def save_careprof(request, object_id, save_person):
    """
    This view function returns the informations about CareProfessional 
    @param request: this is a request sent by the browser.
    @type request: a instance of the class C{HttpRequest} created by the framework Django
    @param object: it is the tyoe of CareProfessional that must be filled.
    @type object: an instance of the built-in type C{CareProfessional}.            
    """
    user = request.user
    object = get_object_or_None(CareProfessional, pk=object_id) or CareProfessional()
    if save_person:
        object.person = person_save(request, get_object_or_None(Person, pk=object.person_id) or Person())
    object.save()

    if (len(request.POST.getlist('professional_service'))):
        for o in object.prof_services.filter(organization=user.get_profile().org_active):
            object.prof_services.remove(o)
        for ps_id in request.POST.getlist('professional_service'):
            ps = Service.objects.get(pk=ps_id)
            object.prof_services.add(ps)

    profile = get_object_or_None(ProfessionalProfile, pk=object.professionalProfile_id) or ProfessionalProfile()
    profile.initialProfessionalActivities = request.POST.get('professional_initialActivitiesDate')
    profile.save()
    object.professionalProfile = profile

    if (len(request.POST.getlist('professional_agreement'))):
        profile.agreement.clear()
        for agreemt_id in request.POST.getlist('professional_agreement'):
            profile.agreement.add(Agreement.objects.get(pk=agreemt_id))

    if (len(request.POST.getlist('professional_workplace'))):
        for o in profile.workplace.filter(organization=user.get_profile().org_active):
            profile.workplace.remove(o)
        for wplace_id in request.POST.getlist('professional_workplace'):
            profile.workplace.add(Place.objects.get(pk=wplace_id))

    identification = get_object_or_None(ProfessionalIdentification, pk=object.professionalIdentification_id) or ProfessionalIdentification()
    identification.profession = get_object_or_None(Profession, symbol=request.POST.get('professional_area'))
    identification.registerNumber = request.POST.get('professional_registerNumber')
    identification.save()
    object.professionalIdentification = identification   

    object.save()
    return object

@permission_required_with_403('careprofessional.careprofessional_write')
def save(request, object_id='', save_person=True):
    object = save_careprof(request, object_id, save_person)
    request.user.message_set.create(message=_('Professional saved successfully'))
    return HttpResponseRedirect('/careprofessional/%s/' % object.id)

def order(request, object_id = ''):
    object = CareProfessional.objects.get(pk = object_id)

    if (object.person.active == True):
        object.person.active = False
    else:
        object.person.active = True

    object.person.save(force_update=True)
    return HttpResponseRedirect('/careprofessional/%s/' % object.id)
