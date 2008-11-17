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

def index(request):
    
    total= []
    
    #list_of_orgs= []
    #for orgs in Organization.objects.all():
     #   orgs= {}
      #  orgs['organization']= orgs
       # list_of_orgs.append( orgs )
        #total.append( orgs )
    
    list_of_places= []
    for places in Place.objects.all():
        places= {}
        places['places']= places
        list_of_places.append( places )
        total.append( places )
    
    list_of_pers= []    
    for persons in Person.objects.all():
        persons= {}
        persons['person']= persons
        list_of_pers.append( persons )
        total.append( persons )
        
         
    return render_to_response('contact/contact_index.html', { 'object': total,
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
    if request.POST['type'] == 'professional':
        try:
            object = get_object_or_404(CareProfessional, pk=object_id)
        except Http404:
            
            person = Person()
            object = CareProfessional()
            person.organization = user.org_active
            person.name = request.POST['professional_name']
            person.nickname = request.POST['professional_name']
            person.save()
            object.person = person
            object.save()
            
        
    return HttpResponse(request.POST['professional_name'])
