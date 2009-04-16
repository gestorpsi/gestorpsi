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

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required
from gestorpsi.person.models import Person, MaritalStatus
from gestorpsi.careprofessional.models import ProfessionalProfile, LicenceBoard, ProfessionalIdentification, CareProfessional
from gestorpsi.organization.models import Agreement
from gestorpsi.phone.models import PhoneType
from gestorpsi.address.models import Country, State, AddressType
from gestorpsi.internet.models import EmailType, IMNetwork
from gestorpsi.document.models import TypeDocument, Issuer
from gestorpsi.place.models import Place, PlaceType
from gestorpsi.person.views import person_save
from gestorpsi.service.models import Service

PROFESSIONAL_AREAS = (
    ('psycho','Psychologist','CRP'),
    )  

@permission_required('professional.professional_list', '/')
def index(request):
    user = request.user
    return render_to_response('careprofessional/careprofessional_index.html', {
                                    'object': CareProfessional.objects.filter(person__organization = user.get_profile().org_active.id).order_by('person__name'),
                                    'PROFESSIONAL_AREAS': PROFESSIONAL_AREAS,
                                    'licenceBoardTypes': LicenceBoard.objects.all(),
                                    'AgreementTypes': Agreement.objects.all(),
                                    'WorkPlacesTypes': Place.objects.filter(organization = user.get_profile().org_active.id),
                                    'countries': Country.objects.all(),
                                    'PhoneTypes': PhoneType.objects.all(),
                                    'AddressTypes': AddressType.objects.all(),
                                    'EmailTypes': EmailType.objects.all(),
                                    'IMNetworks': IMNetwork.objects.all(),
                                    'TypeDocuments': TypeDocument.objects.all(),
                                    'Issuers': Issuer.objects.all(),
                                    'States': State.objects.all(),
                                    'MaritalStatusTypes': MaritalStatus.objects.all(),
                                    'PlaceTypes': PlaceType.objects.all(),
                                    'ServiceTypes': Service.objects.filter( active=True, organization=user.get_profile().org_active ),
                                    },
                                context_instance=RequestContext(request)
                              )
  

@permission_required('professional.professional_read', '/')
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
        #services = object.professionalProfile.services.all()
    except:
        object = CareProfessional() 

    return render_to_response('careprofessional/careprofessional_form.html', {
                                    'object': object,
                                    'emails': emails,
                                    'websites': sites,
                                    'ims': instantMessengers,
                                    'addresses': addresses,
                                    'phones': phones,
                                    'documents': documents,
                                    'PROFESSIONAL_AREAS': PROFESSIONAL_AREAS,                                    
                                    'licenceBoardTypes': LicenceBoard.objects.all(),
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
                                    },
                              context_instance=RequestContext(request)
                              )

def care_professional_fill(request, object):
    """
    This view function returns the informations about CareProfessional 
    @param request: this is a request sent by the browser.
    @type request: a instance of the class C{HttpRequest} created by the framework Django
    @param object: it is the tyoe of CareProfessional that must be filled.
    @type object: an instance of the built-in type C{Psychologist}.            
    """
    try:
        person= Person.objects.get(pk=object.person_id)        
    except:        
        person= Person()
    object.person= person_save(request, person)   
    object.save()
    try:
        profile= ProfessionalProfile.objects.get(pk= object.professionalProfile_id )        
    except:        
        profile= ProfessionalProfile()
    
    if ( len( request.POST.getlist( 'professional_service' ) ) ):
        object.prof_services.clear()
        for ps_id in request.POST.getlist( 'professional_service' ):
            ps = Service.objects.get(pk=ps_id)
            object.prof_services.add(ps)

    profile.initialProfessionalActivities = request.POST[ 'professional_initialActivitiesDate' ]
    profile.availableTime = request.POST['professional_availableTime']
    profile.save()

    if ( len( request.POST.getlist( 'professional_agreement' ) ) ):
        profile.agreement.clear()
        for agreemt_id in request.POST.getlist( 'professional_agreement' ):
               agreemt= Agreement.objects.get( pk= agreemt_id )
               profile.agreement.add( agreemt )

    if ( len(request.POST.getlist( 'professional_workplace' ) ) ):
        profile.workplace.clear()
        for wplace_id in request.POST.getlist( 'professional_workplace' ):
            wplace= Place.objects.get( pk= wplace_id )
            profile.workplace.add( wplace )

    object.professionalProfile= profile

    try:
        identification =  ProfessionalIdentification.objects.get(pk = object.professionalIdentification_id )
    except:
        identification = ProfessionalIdentification()

    try:
        identification.licenceBoard = LicenceBoard.objects.get(pk=request.POST['professional_licenceBoard'])
    except:
        identification.licenceBoard = None

    identification.registerNumber = request.POST['professional_registerNumber']
    identification.save()
    object.professionalIdentification = identification   

    return object