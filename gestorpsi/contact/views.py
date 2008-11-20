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


def index(request):
    user = request.user
    org = user.org_active
    
    lista = [] # ID, Name, Email, Phone, ORG/PROF, GESTORPSI/LOCAL
    
    for x in Organization.objects.filter(organization=None, public=True):
        phone = x.get_first_phone()
        email = x.get_first_email()
        lista.append([x.id, x.name, email, phone, 'ORG', 'GESTORPSI'])
        
        for y in CareProfessional.objects.filter(person__organization=x):
            phone = y.person.get_first_phone()
            email = y.person.get_first_email()
            lista.append([y.id, y.person.name, email, phone, 'PROF', 'GESTORPSI'])
    
    for x in Organization.objects.filter(organization=org):
        phone = x.get_first_phone()
        email = x.get_first_email()
        lista.append([x.id, x.name, email, phone, 'ORG', 'LOCAL'])
        
        for y in CareProfessional.objects.filter(person__organization=x):
            phone = y.person.get_first_phone()
            email = y.person.get_first_email()
            lista.append([y.id, y.person.name, email, phone, 'PROF', 'LOCAL'])            
        
    for x in lista:
        print u"%s" % x

    return render_to_response('contact/contact_index.html', { 
                                    'objects': lista,
                                    'countries': Country.objects.all(),
                                    'PhoneTypes': PhoneType.objects.all(), 
                                    'AddressTypes': AddressType.objects.all(), 
                                    'EmailTypes': EmailType.objects.all(), 
                                    'IMNetworks': IMNetwork.objects.all() , 
                                    'States': State.objects.all(), 
                                    })


def form(request):
    return render_to_response('contact/contact_form.html')

def save(request, object_id=''):
    user = request.user
    if request.POST['type'] == 'organization':
        try:
            object = get_object_or_404(Organization, pk=object_id)
        except:
            object = Organization()
        object.name = request.POST['organization_name']
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
        
        person.name = request.POST['professional_name']
        #person.organization = Organization.objects.get(pk=request.POST['organization'])
        person.organization = Organization.objects.get(pk='29a6b2f3-f0e5-41c3-8870-6a35c23238f1')
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
