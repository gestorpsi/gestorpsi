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
from django.template.context import RequestContext
from gestorpsi.organization.models import Agreement
from gestorpsi.careprofessional.models import CareProfessional, ProfessionalProfile,  LicenceBoard, ProfessionalIdentification
from gestorpsi.address.models import Country, State, AddressType
from gestorpsi.phone.models import PhoneType
from gestorpsi.internet.models import EmailType, IMNetwork
from gestorpsi.document.models import TypeDocument, Issuer
from gestorpsi.person.models import Person, MaritalStatus
from gestorpsi.place.models import Place, PlaceType
from gestorpsi.person.views import person_type_url 
from gestorpsi.authentication.models import Profile
from gestorpsi.person.models import Person
from gestorpsi.service.models import Service

import datetime

PROFESSIONAL_AREAS = (
    ('psycho','Psychologist','CRP'),
    )


def form(request):
    #if(request.user.is_authenticated()):
    # COMMON FOR ALL PERSON
    user = request.user
    profile = user.get_profile()
    preferences = person_type_url(user.get_profile().person)
    print preferences
    date = datetime.datetime.now()
    phones = profile.person.phones.all()
    addresses= profile.person.address.all()
    documents = profile.person.document.all()                       
    emails = profile.person.emails.all()
    sites = profile.person.sites.all()
    instantMessengers = profile.person.instantMessengers.all()

################################## CAREPROFESSIONAL
    try:
        workplaces = profile.person.careprofessional.professionalProfile.workplace.all()
        agreements = profile.person.careprofessional.professionalProfile.agreement.all()

        identification =  profile.person.careprofessional
        return render_to_response('profile/profile_index.html', { 
                                        'object': profile,
                                        'profile': profile,
                                        'preferences': preferences,
                                        'date': date,
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
                                        'object': identification,
                                        },
                                    context_instance=RequestContext(request)
                                      )
    except:
        pass

################################## EMPLOYEE
    try:
        identification =  profile.person.employee
        return render_to_response('profile/profile_index.html', { 
                                        'object': profile,
                                        'profile': profile,
                                        'preferences': preferences,
                                        'date': date,
                                        'emails': emails,
                                        'websites': sites,
                                        'ims': instantMessengers,
                                        'addresses': addresses,
                                        'phones': phones,
                                        'documents': documents,
                                        'countries': Country.objects.all(),
                                        'PhoneTypes': PhoneType.objects.all(),
                                        'AddressTypes': AddressType.objects.all(),
                                        'EmailTypes': EmailType.objects.all(),
                                        'IMNetworks': IMNetwork.objects.all() ,
                                        'TypeDocuments': TypeDocument.objects.all(),
                                        'Issuers': Issuer.objects.all(),
                                        'States': State.objects.all(),
                                        'PlaceTypes': PlaceType.objects.all(),
                                        'object': identification,
                                        },
                                    context_instance=RequestContext(request)
                                    )
    except:
        pass
    
################################## CLIENT
    try:
        identification =  profile.person.client
        return render_to_response('profile/profile_index.html', { 
                                        'object': profile,
                                        'profile': profile,
                                        'preferences': preferences,
                                        'date': date,
                                        'emails': emails,
                                        'websites': sites,
                                        'ims': instantMessengers,
                                        'addresses': addresses,
                                        'phones': phones,
                                        'documents': documents,
                                        'countries': Country.objects.all(),
                                        'PhoneTypes': PhoneType.objects.all(),
                                        'AddressTypes': AddressType.objects.all(),
                                        'EmailTypes': EmailType.objects.all(),
                                        'IMNetworks': IMNetwork.objects.all() ,
                                        'TypeDocuments': TypeDocument.objects.all(),
                                        'Issuers': Issuer.objects.all(),
                                        'States': State.objects.all(),
                                        'PlaceTypes': PlaceType.objects.all(),
                                        'object': identification,
                                        },
                                    context_instance=RequestContext(request)
                                    )
    except:
        pass
