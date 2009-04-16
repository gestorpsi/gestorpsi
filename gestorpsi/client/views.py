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
from django.contrib.auth.decorators import permission_required
from django.conf import settings
from geraldo.generators import PDFGenerator
from gestorpsi.client.models import Client, IdRecordSeq
from gestorpsi.person.models import Person, MaritalStatus
from gestorpsi.phone.models import PhoneType
from gestorpsi.address.models import Country, State, AddressType
from gestorpsi.internet.models import EmailType, IMNetwork
from gestorpsi.document.models import TypeDocument, Issuer
from gestorpsi.person.views import person_save
from gestorpsi.client.reports import ClientRecord, ClientList
from gestorpsi.reports.header import header_gen
from gestorpsi.reports.footer import footer_gen

# list all active clients
@permission_required('client.client_list', '/')
def index(request):
    user = request.user
    object = Client.objects.filter(person__organization = user.get_profile().org_active.id, clientStatus = '1').order_by('person__name')
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

@permission_required('client.client_list', '/')
def list(request, page = 1):
    user = request.user
    object = Client.objects.filter(person__organization = user.get_profile().org_active.id, clientStatus = '1').order_by('person__name')
    paginator = Paginator(object, settings.PAGE_RESULTS)
    object = paginator.page(page)
    return render_to_response('client/client_list.html',
                                {'object': object,
                                 'paginator': paginator,
                                },
                              context_instance=RequestContext(request)            
                              )


# add or edit form
@permission_required('client.client_read', '/')
def form(request, object_id=''):
    phones    = []
    addresses = []
    documents = []
    emails    = []
    sites     = []
    instantMessengers = []
    last_update = ''

    try:
        object    = get_object_or_404(Client, pk=object_id)        
        phones    = object.person.phones.all()
        addresses = object.person.address.all()
        documents = object.person.document.all()
        emails    = object.person.emails.all()
        sites     = object.person.sites.all()
        instantMessengers = object.person.instantMessengers.all()
        #last_update = object.history.latest('_audit_timestamp')._audit_timestamp
    except:
        object = Client()
    
    return render_to_response('client/client_form.html',
                              {'object': object, 'emails': emails, 'websites': sites, 'ims': instantMessengers, 'phones': phones, 'addresses': addresses, 'countries': Country.objects.all(), 'PhoneTypes': PhoneType.objects.all(), 'AddressTypes': AddressType.objects.all(), 'EmailTypes': EmailType.objects.all(), 'IMNetworks': IMNetwork.objects.all() , 'documents': documents, 'TypeDocuments': TypeDocument.objects.all(), 'Issuers': Issuer.objects.all(), 'States': State.objects.all(), 'MaritalStatusTypes': MaritalStatus.objects.all(), 'last_update': last_update },
                              context_instance=RequestContext(request)
                              )

# Save or Update client object
@permission_required('client.client_write', '/')
def save(request, object_id=""):

    try:
        object = get_object_or_404(Client, pk=object_id)
        person = object.person
    except Http404:
        object = Client()
        person = Person()

    object.person = person_save(request, person)
    object.save()

    """ Id Record """
    idr = IdRecordSeq()
    idr.uid = object.id
    idr.save()

    return HttpResponse(object.id)

# delete (disable) a client
def delete(request, object_id=""):
    client = get_object_or_404(Client, pk=object_id)
    client.clientStatus = '0'
    client.save()
    return render_to_response('client/client_index.html', {'clientList': Client.objects.all().filter(clientStatus = '1') })

@permission_required('client.client_list', '/')
def print_list(request):
    user = request.user
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=clients.pdf'
    object = Client.objects.filter(person__organization = user.get_profile().org_active.id, clientStatus = '1').order_by('person__name')
    report = ClientList(queryset=object)
    report.title = "Client List"
    report.band_page_header = header_gen(user.get_profile().org_active)
    report.band_page_footer = footer_gen(user.get_profile().org_active)
    report.generate_by(PDFGenerator, filename=response)
    return response

@permission_required('client.client_read', '/')
def print_record(request, object_id):
    user = request.user
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=client.pdf'
    client = Client.objects.filter(pk=object_id)
    report = ClientRecord(queryset=client)
    report.title = "Client Record"
    report.band_page_header = header_gen(organization=user.get_profile().org_active, header_line=False, clinic_info=True)
    report.band_page_footer = footer_gen(organization=user.get_profile().org_active)
    report.generate_by(PDFGenerator, filename=response)
    return response
