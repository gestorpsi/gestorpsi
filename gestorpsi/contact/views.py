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

from django.shortcuts import render_to_response, get_list_or_404, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from gestorpsi.organization.models import Organization
from gestorpsi.phone.models import Phone, PhoneType
from gestorpsi.address.models import Country, City, State, Address, AddressType
from gestorpsi.internet.models import Email, EmailType, InstantMessenger, IMNetwork
from gestorpsi.person.models import Person
from gestorpsi.place.models import Place
from gestorpsi.careprofessional.models import CareProfessional
from gestorpsi.careprofessional.views import care_professional_fill
from gestorpsi.address.views import address_save
from gestorpsi.phone.views import phone_save
from gestorpsi.internet.views import email_save, site_save, im_save
import operator

def list_order(dictionary):
    lista = []
    nl = []
    
    for x in dictionary:
        lista.append([x[1].lower(), x])
    ordered = sorted(lista, key=operator.itemgetter(0))
    for y in ordered:
        nl.append(y[1])
    
    return nl

def index(request):
    user = request.user
    org = user.org_active
    
    lista = [] # ID, Name, Email, Phone, 1(ORG)/2(PROF), 1(GESTORPSI)/2(LOCAL)
    organizations_count = len(address_book_get_organizations(request))
    professionals_count = len(address_book_get_professionals(request))
    
    for i in address_book_get_organizations(request): # append organizations
        lista.append(i)
    for i in address_book_get_professionals(request): # append professionals
        lista.append(i)
    
    
#    for x in (Organization.objects.filter(organization=None, public=True) | Organization.objects.filter(organization=org) ):
#        phone = x.get_first_phone()
#        email = x.get_first_email()
#        if x.organization == None:
#            lista.append([x.id, x.name, email, phone, '1', 'GESTORPSI'])
#        else:
#            lista.append([x.id, x.name, email, phone, '1', 'LOCAL'])
#        
#        for y in CareProfessional.objects.filter(person__organization=x):
#            phone = y.person.get_first_phone()
#            email = y.person.get_first_email()
#            if x.organization == None:
#                lista.append([y.id, y.person.name, email, phone, '2', 'GESTORPSI'])
#            else:
#                lista.append([y.id, y.person.name, email, phone, '2', 'LOCAL'])

    return render_to_response('contact/contact_index.html', { 
                                    'object': list_order(lista),
                                    'organizations_count': organizations_count,
                                    'professionals_count': professionals_count,
                                    'countries': Country.objects.all(),
                                    'States': State.objects.all(),
                                    'AddressTypes': AddressType.objects.all(),
                                    'PhoneTypes': PhoneType.objects.all(),
                                    'EmailTypes': EmailType.objects.all(),
                                    'IMNetworks': IMNetwork.objects.all(),
                                    'States': State.objects.all(),
                                    'organizations': Organization.objects.filter(organization=org)
                                    })


def form(request, object_type='', object_id=''):
    user = request.user
    org = user.org_active

    if object_type == '1':   # ORGANIZATION (1)
        object = get_object_or_404(Organization, pk=object_id)
        phones    = object.phones.all()
        addresses = object.address.all()
        emails    = object.emails.all()
        sites     = object.sites.all()
        instantMessengers = object.instantMessengers.all()
    else:                    # PROFESSIONAL (2)
        object = get_object_or_404(CareProfessional, pk=object_id)
        phones    = object.person.phones.all()
        addresses = object.person.address.all()
        emails    = object.person.emails.all()
        sites     = object.person.sites.all()
        instantMessengers = object.person.instantMessengers.all()
        last_update = object.history.latest('_audit_timestamp')._audit_timestamp
        
    return render_to_response('contact/contact_form.html', {
                                    'object': object,
                                    'object_type': object_type,
                                    'countries': Country.objects.all(),
                                    'States': State.objects.all(),
                                    'AddressTypes': AddressType.objects.all(),
                                    'PhoneTypes': PhoneType.objects.all(), 
                                    'EmailTypes': EmailType.objects.all(), 
                                    'IMNetworks': IMNetwork.objects.all(),
                                    'organizations': Organization.objects.filter(organization=org),
                                    'emails': emails,
                                    'websites': sites,
                                    'ims': instantMessengers,
                                    'phones': phones,
                                    'addresses': addresses,
                                     })

def save(request, object_id=''):
    user = request.user
    if request.POST['type'] == 'organization':
        try:
            object = get_object_or_404(Organization, pk=object_id)
        except:
            object = Organization()
        
        try:
            object.name = request.POST['label'] # adding by mini form
        except:
            object.name = request.POST['name']
        
        object.organization = user.org_active
        
        object.save()
        
        phone_save(object, request.POST.getlist('phoneId'), request.POST.getlist('area'), request.POST.getlist('phoneNumber'), request.POST.getlist('ext'), request.POST.getlist('phoneType'))
        email_save(object, request.POST.getlist('email_id'), request.POST.getlist('email_email'), request.POST.getlist('email_type'))
        site_save(object, request.POST.getlist('site_id'), request.POST.getlist('site_description'), request.POST.getlist('site_site'))
        im_save(object, request.POST.getlist('im_id'), request.POST.getlist('im_identity'), request.POST.getlist('im_network'))
        address_save(object, request.POST.getlist('addressId'), request.POST.getlist('addressPrefix'),
                 request.POST.getlist('addressLine1'), request.POST.getlist('addressLine2'),
                 request.POST.getlist('addressNumber'), request.POST.getlist('neighborhood'),
                 request.POST.getlist('zipCode'), request.POST.getlist('addressType'),
                 request.POST.getlist('city'), request.POST.getlist('foreignCountry'),
                 request.POST.getlist('foreignState'), request.POST.getlist('foreignCity'))        

    if request.POST['type'] == 'professional':
        try:
            object = get_object_or_404(CareProfessional, pk=object_id)
            person = object.person
        except:
            object = CareProfessional()
            person = Person()
        person.name = request.POST['name']
        person.organization = Organization.objects.get(pk=request.POST['organization'])
        person.save()

        phone_save(person, request.POST.getlist('phoneId'), request.POST.getlist('area'), request.POST.getlist('phoneNumber'), request.POST.getlist('ext'), request.POST.getlist('phoneType'))
        email_save(person, request.POST.getlist('email_id'), request.POST.getlist('email_email'), request.POST.getlist('email_type'))
        site_save(person, request.POST.getlist('site_id'), request.POST.getlist('site_description'), request.POST.getlist('site_site'))
        im_save(person, request.POST.getlist('im_id'), request.POST.getlist('im_identity'), request.POST.getlist('im_network'))
        address_save(person, request.POST.getlist('addressId'), request.POST.getlist('addressPrefix'),
                 request.POST.getlist('addressLine1'), request.POST.getlist('addressLine2'),
                 request.POST.getlist('addressNumber'), request.POST.getlist('neighborhood'),
                 request.POST.getlist('zipCode'), request.POST.getlist('addressType'),
                 request.POST.getlist('city'), request.POST.getlist('foreignCountry'),
                 request.POST.getlist('foreignState'), request.POST.getlist('foreignCity'))        
        
        object.person = person
        object.save()
    
    return HttpResponse(object.id)


def address_book_get_professionals(request):
    user = request.user
    org = user.org_active
    lista = []
    
    for x in Organization.objects.filter(organization=None, public=True):
        phone = x.get_first_phone()
        email = x.get_first_email()
        for y in CareProfessional.objects.filter(person__organization=x):
            phone = y.person.get_first_phone()
            email = y.person.get_first_email()
            lista.append([y.id, '%s (%s)' % (y.person.name, y.person.organization), email, phone, '2', 'GESTORPSI'])
    
    for x in Organization.objects.filter(organization=org):
        phone = x.get_first_phone()
        email = x.get_first_email()
        for y in CareProfessional.objects.filter(person__organization=x):
            phone = y.person.get_first_phone()
            email = y.person.get_first_email()
            lista.append([y.id, '%s (%s)' % (y.person.name, y.person.organization), email, phone, '2', 'LOCAL'])

    return lista

def address_book_get_organizations(request):
    user = request.user
    org = user.org_active
    lista = []
    
    for x in Organization.objects.filter(organization=None, public=True):
        phone = x.get_first_phone()
        email = x.get_first_email()
        lista.append([x.id, x.name, email, phone, '1', 'GESTORPSI'])

    for x in Organization.objects.filter(organization=org):
        phone = x.get_first_phone()
        email = x.get_first_email()
        lista.append([x.id, x.name, email, phone, '1', 'LOCAL'])

    return lista

#def save(request, object_id=''):
#    user = request.user
#
#    if request.POST['type'] == 'professional':
#        try:
#            object = get_object_or_404(CareProfessional, pk=object_id)
#        except Http404:
#            
#            person = Person()
#            object = CareProfessional()
#            person.organization = user.org_active
#            person.name = request.POST['professional_name']
#            person.nickname = request.POST['professional_name']
#            person.save()
#            object.person = person
#            object.save()
#            
#    if request.POST['type'] == 'organization':
#        print "fdsfds"
#        
#    return HttpResponse(request.POST['professional_name'])
