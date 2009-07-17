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

import locale
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils.translation import gettext as _

from geraldo.generators import PDFGenerator

from gestorpsi.address.models import Country, State, AddressType
from gestorpsi.admission.models import *
from gestorpsi.authentication.models import Profile
from gestorpsi.careprofessional.models import LicenceBoard, CareProfessional
from gestorpsi.service.models import Service
from gestorpsi.careprofessional.views import Profession
from gestorpsi.client.models import Client, PersonLink, Relation
from gestorpsi.client.reports import ClientRecord, ClientList
from gestorpsi.document.models import TypeDocument, Issuer
from gestorpsi.internet.models import EmailType, IMNetwork
from gestorpsi.organization.models import Organization
from gestorpsi.person.models import Person, MaritalStatus
from gestorpsi.person.views import person_save
from gestorpsi.phone.models import PhoneType
from gestorpsi.referral.models import Referral
from gestorpsi.referral.forms import ReferralForm
from gestorpsi.reports.header import header_gen
from gestorpsi.reports.footer import footer_gen
from django.utils import simplejson
from gestorpsi.util.decorators import permission_required_with_403
from gestorpsi.person.views import person_json_list

# list all active clients
@permission_required_with_403('client.client_list')
def index(request):
    # Test if clinic administrator has registered services before access client page.
    if not Service.objects.filter(active=True, organization=request.user.get_profile().org_active).count():
        return render_to_response('client/client_service_alert.html', {'object': _("There's no Service created yet. Please, create one before access Client."), }, context_instance=RequestContext(request))

    referral_form = ReferralForm()
    referral_form.fields['service'].queryset = Service.objects.filter(active=True, organization=request.user.get_profile().org_active)
    #referral_form.fields['professional'].queryset = CareProfessional.objects.filter(person__organization = request.user.get_profile().org_active.id)
    referral_form.fields['client'].queryset = Client.objects.filter(person__organization = request.user.get_profile().org_active.id, clientStatus = '1')

    return render_to_response('client/client_index.html',
                                        {
                                        'countries': Country.objects.all(),
                                        'PhoneTypes': PhoneType.objects.all(), 
                                        'AddressTypes': AddressType.objects.all(), 
                                        'EmailTypes': EmailType.objects.all(), 
                                        'IMNetworks': IMNetwork.objects.all() , 
                                        'TypeDocuments': TypeDocument.objects.all(), 
                                        'Issuers': Issuer.objects.all(), 
                                        'States': State.objects.all(), 
                                        'MaritalStatusTypes': MaritalStatus.objects.all(),
                                        'PROFESSIONAL_AREAS': Profession.objects.all(),
                                        'licenceBoardTypes': LicenceBoard.objects.all(),
                                        'ReferralChoices': ReferralChoice.objects.all(),
                                        'IndicationsChoices': IndicationChoice.objects.all(),
                                        'Relations': Relation.objects.all(),
                                        'referral_form': referral_form
                                         },
                                        context_instance=RequestContext(request))

@permission_required_with_403('client.client_list')
def list(request, page = 1):
    user = request.user
    if user.groups.filter(name='administrator').count() == 1 or user.groups.filter(name='secretary').count() == 1:
        object = Client.objects.filter(person__organization = user.get_profile().org_active.id, clientStatus = '1').order_by('person__name')
    else:
        object = Client.objects.filter(person__organization = user.get_profile().org_active.id, clientStatus = '1', referral__professional = user.profile.person.careprofessional.id).order_by('person__name')
    
    return HttpResponse(simplejson.dumps(person_json_list(request, object, 'client.client_read', page)),
                            mimetype='application/json')

# add or edit form
@permission_required_with_403('client.client_read')
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
        
    # User Registration Code
    groups = [False, False, False, False]
    try:
        profile = get_object_or_404(Profile, person=object.person.id)
        for g in profile.user.groups.all():
            if g.name == "administrator": groups[0] = True
            if g.name == "psychologist":  groups[1] = True
            if g.name == "secretary":     groups[2] = True
            if g.name == "client":        groups[3] = True
    except:
        profile = Profile()
        profile.person = get_object_or_404(Person, pk=object.person.id)
        profile.user = User(username=slugify(profile.person.name))

    # client referral
    data = {'client': [object.id]}
    referral_form = ReferralForm(data)
    referral_form.fields['referral'].queryset = Referral.objects.filter(client=object)
    referral_form.fields['service'].queryset = Service.objects.filter(active=True, organization=request.user.get_profile().org_active)
    #referral_form.fields['professional'].queryset = CareProfessional.objects.filter(person__organization = request.user.get_profile().org_active.id)
    referral_form.fields['client'].queryset = Client.objects.filter(person__organization = request.user.get_profile().org_active.id, clientStatus = '1')
    total_service = Referral.objects.filter(client=object).count()
    referral_list = Referral.objects.filter(client=object, status='01')
    
    return render_to_response('client/client_form.html',
                              {'object': object, 
                                'emails': emails, 
                                'websites': sites, 
                                'ims': instantMessengers, 
                                'phones': phones, 
                                'addresses': addresses, 
                                'countries': Country.objects.all(), 
                                'PhoneTypes': PhoneType.objects.all(), 
                                'AddressTypes': AddressType.objects.all(), 
                                'EmailTypes': EmailType.objects.all(), 
                                'IMNetworks': IMNetwork.objects.all(), 
                                'documents': documents, 
                                'TypeDocuments': TypeDocument.objects.all(), 
                                'Issuers': Issuer.objects.all(), 
                                'States': State.objects.all(), 
                                'MaritalStatusTypes': MaritalStatus.objects.all(), 
                                'last_update': last_update,
                                'PROFESSIONAL_AREAS': Profession.objects.all(),
                                'licenceBoardTypes': LicenceBoard.objects.all(),
                                'ReferralChoices': ReferralChoice.objects.all(),
                                'IndicationsChoices': IndicationChoice.objects.all(),
                                'Relations': Relation.objects.all(),
                                'referral_form': referral_form,
                                'referral_list': referral_list,
                                'referrals': Referral.objects.filter(client = object),
                                'profile': profile,
                                'groups': groups,
                                'total_service': total_service,
                                'list_org': Organization.objects.filter(active=True, visible=True),
                                'list_prof': CareProfessional.objects.all(),
                               },
                              context_instance=RequestContext(request)
                              )

@permission_required_with_403('client.client_write')
def save(request, object_id=""):
    """
       Save or Update a client record
    """
    user = request.user

    try:
        object = get_object_or_404(Client, pk=object_id)
        person = object.person
    except Http404:
        object = Client()
        person = Person()
        
        # Id Record
        org = get_object_or_404(Organization, pk=user.get_profile().org_active.id )
        object.idRecord = org.last_id_record + 1
        org.last_id_record = org.last_id_record + 1
        org.save()

    object.person = person_save(request, person)
    object.save()

    return HttpResponse(object.id)

@permission_required_with_403('client.client_write')
def delete(request, object_id=""):
    client = get_object_or_404(Client, pk=object_id)
    client.clientStatus = '0'
    client.save()
    return render_to_response('client/client_index.html', {'clientList': Client.objects.all().filter(clientStatus = '1') })

@permission_required_with_403('client.client_list')
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

@permission_required_with_403('client.client_read')
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

@permission_required_with_403('client.client_read')
def organization_clients(request):
    """
       organization_clients: return json with all clients from logged organization
    """
    user = request.user
    clients = Client.objects.filter(person__organization = user.get_profile().org_active.id, clientStatus = '1', person__name__istartswith=request.GET.get('q') ).order_by('person__name')

    dict = {}
    array = [] #json
    i = 0

    for o in clients:
        c = {
            'id': o.id,
            'name': o.person.name,
        }
        array.append(c)

    dict['results'] = array
    array = simplejson.dumps(dict, encoding = 'iso8859-1')

    return HttpResponse(array, mimetype='application/json')
