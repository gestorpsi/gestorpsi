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

import operator

from gestorpsi.address.models import City
from gestorpsi.address.views import address_save
from gestorpsi.document.views import document_save
from gestorpsi.person.models import MaritalStatus
from gestorpsi.phone.views import phone_save
from gestorpsi.internet.views import email_save, site_save, im_save
from gestorpsi.util.views import date_form_to_db

def person_save(request, person):
    person.name= request.POST['name']
    person.nickname = request.POST['nickname']

    if(request.POST['photo']):
        person.photo = request.POST['photo']
    else:
        person.photo = ''

    if(request.POST['birthDate']):
        person.birthDate = date_form_to_db(request.POST['birthDate'])

    person.gender = request.POST['gender']
    
    # maritalStatus
    try:
        if not (request.POST['maritalStatus']):
            person.maritalStatus = None
        else:
            person.maritalStatus = MaritalStatus.objects.get(pk = request.POST['maritalStatus'])
    except:
        person.maritalStatus = None

    # birthPlace (Naturality)
    person.birthForeignCity= ''
    person.birthForeignState= ''
    person.birthForeignCountry= None
    
    if not (request.POST['birthPlace']):
        person.birthPlace = None
        if( request.POST['birthForeignCity']):
            person.birthForeignCity= request.POST['birthForeignCity']
        if( request.POST['birthForeignState'] ):
            person.birthForeignState= request.POST['birthForeignState']
        try:
            person.birthForeignCountry= request.POST['birthForeignCountry']
        except:
            person.birthForeignCountry= None
    else:
        person.birthPlace = City.objects.get(pk = request.POST['birthPlace'])

    user = request.user
    person.organization = user.org_active    
    person.save()

    # save phone numbers (using Phone APP)
    phone_save(person, request.POST.getlist('phoneId'), request.POST.getlist('area'), request.POST.getlist('phoneNumber'), request.POST.getlist('ext'), request.POST.getlist('phoneType'))

    # save addresses (using Address APP)
    address_save(person, request.POST.getlist('addressId'), request.POST.getlist('addressPrefix'),
                 request.POST.getlist('addressLine1'), request.POST.getlist('addressLine2'),
                 request.POST.getlist('addressNumber'), request.POST.getlist('neighborhood'),
                 request.POST.getlist('zipCode'), request.POST.getlist('addressType'),
                 request.POST.getlist('city'), request.POST.getlist('foreignCountry'),
                 request.POST.getlist('foreignState'), request.POST.getlist('foreignCity'))
    
    # save documents (using Document APP) 
    document_save(person, request.POST.getlist('documentId'), request.POST.getlist('document_typeDocument'), request.POST.getlist('document_document'), request.POST.getlist('document_issuer'), request.POST.getlist('document_state'))
    
    # save internet data
    email_save(person, request.POST.getlist('email_id'), request.POST.getlist('email_email'), request.POST.getlist('email_type'))
    site_save(person, request.POST.getlist('site_id'), request.POST.getlist('site_description'), request.POST.getlist('site_site'))
    im_save(person, request.POST.getlist('im_id'), request.POST.getlist('im_identity'), request.POST.getlist('im_network'))

    return person

def person_order(dictionary):
    lista = []
    nl = []
    
    for x in dictionary:
        lista.append([x.person.name.lower(), x])
    ordered = sorted(lista, key=operator.itemgetter(0))
    for y in ordered:
        nl.append(y[1])
    
    return nl