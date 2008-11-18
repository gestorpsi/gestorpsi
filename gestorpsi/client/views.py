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

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator
from django.conf import settings
from gestorpsi.client.models import Client
from gestorpsi.person.models import Person, MaritalStatus
from gestorpsi.phone.models import Phone, PhoneType
from gestorpsi.address.models import Country, City, State, Address, AddressType
from gestorpsi.internet.models import Email, EmailType, InstantMessenger, IMNetwork
from gestorpsi.document.models import Document, TypeDocument, Issuer
from gestorpsi.person.views import person_save
from gestorpsi.careprofessional.models import Profession, ProfessionalProfile, LicenceBoard, ProfessionalIdentification, CareProfessional
from gestorpsi.careprofessional.views import PROFESSIONAL_AREAS

# list all active clients
def index(request):
    user = request.user
    object = Client.objects.filter(person__organization = user.org_active.id, clientStatus = '1')
    paginator = Paginator(object, settings.PAGE_RESULTS)
    object = paginator.page(1)
    return render_to_response('client/client_index.html',
                                {'object': object,
                                 'paginator': paginator,
                                'countries': Country.objects.all(),
                                'PhoneTypes': PhoneType.objects.all(), 
                                'AddressTypes': AddressType.objects.all(), 
                                'EmailTypes': EmailType.objects.all(), 
                                'IMNetworks': IMNetwork.objects.all() , 
                                'TypeDocuments': TypeDocument.objects.all(), 
                                'Issuers': Issuer.objects.all(), 
                                'States': State.objects.all(), 
                                'MaritalStatusTypes': MaritalStatus.objects.all(), },
                              context_instance=RequestContext(request)            
                              )

def list(request, page = 1):
    user = request.user
    object = Client.objects.filter(person__organization = user.org_active.id, clientStatus = '1')
    paginator = Paginator(object, settings.PAGE_RESULTS)
    object = paginator.page(page)
    return render_to_response('client/client_list.html',
                                {'object': object,
                                 'paginator': paginator,
                                },
                              context_instance=RequestContext(request)            
                              )


# add or edit form
def form(request, object_id=''):
    phones    = []
    addresses = []
    documents = []
    emails    = []
    sites     = []
    instantMessengers = []
    try:
        object    = get_object_or_404(Client, pk=object_id)        
        phones    = object.person.phones.all()
        addresses = object.person.address.all()
        documents = object.person.document.all()
        emails    = object.person.emails.all()
        sites     = object.person.sites.all()
        instantMessengers = object.person.instantMessengers.all()
        last_update = object.history.latest('_audit_timestamp')._audit_timestamp
    except:
        object = Client()
    
    return render_to_response('client/client_form.html',
                              {'object': object, 'emails': emails, 'websites': sites, 'ims': instantMessengers, 'phones': phones, 'addresses': addresses, 'countries': Country.objects.all(), 'PhoneTypes': PhoneType.objects.all(), 'AddressTypes': AddressType.objects.all(), 'EmailTypes': EmailType.objects.all(), 'IMNetworks': IMNetwork.objects.all() , 'documents': documents, 'TypeDocuments': TypeDocument.objects.all(), 'Issuers': Issuer.objects.all(), 'States': State.objects.all(), 'MaritalStatusTypes': MaritalStatus.objects.all(), 'last_update': last_update },
                              context_instance=RequestContext(request)
                              )

def form_admission(request, object_id=''):
    return render_to_response('client/client_admission.html', {
        'CareProfessionals': CareProfessional.objects.all(),
        'PROFESSIONAL_AREAS': PROFESSIONAL_AREAS,
        'licenceBoardTypes': LicenceBoard.objects.all(),
    })

# Save or Update client object
def save(request, object_id=""):

    try:
        object = get_object_or_404(Client, pk=object_id)
        person = object.person
    except Http404:
        object = Client()
        person = Person()

    object.person = person_save(request, person)
    object.save()

    return HttpResponse(object.id)

# delete (disable) a client
def delete(request, object_id=""):
    client = get_object_or_404(Client, pk=object_id)
    client.clientStatus = '0'
    client.save()
    return render_to_response('client/client_index.html', {'clientList': Client.objects.all().filter(clientStatus = '1') })
