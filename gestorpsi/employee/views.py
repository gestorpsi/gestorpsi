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
from gestorpsi.employee.models import Employee
from gestorpsi.person.models import Person, MaritalStatus
from gestorpsi.phone.models import Phone, PhoneType
from gestorpsi.address.models import Country, City, State, Address, AddressType
from gestorpsi.internet.models import Email, EmailType, InstantMessenger, IMNetwork
from gestorpsi.document.models import Document, TypeDocument, Issuer
from gestorpsi.person.views import person_save

def index(request):
    """
    This view function returns a list that contains all employees currently in the system.
    @param request: this is a request sent by the browser.
    @type request: a instance of the class C{HttpRequest} created by the framework Django
    """ 
    user = request.user
    
    return render_to_response('employee/employee_index.html',
                            {'object': Employee.objects.filter(person__organization = user.org_active.id, active = True), 
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

def form(request, object_id= ''):
    """
    This function view creates an employee form. If the object_id has a value, this form will be fill with employee information.
    otherwise, a new form will be create
    @param request: this is a request sent by the browser.
    @type request: an instance of the class C{HttpRequest} created by the framework Django.
    @param object_id: it is the I{id} of the employee that must be saved.
    @type object_id: an instance of the built-in type C{int}. 
    """
    phones    = []
    addresses = []
    documents = []
    emails    = []
    sites     = []
    instantMessengers = []    
    try:
        object    = get_object_or_404(Employee, pk=object_id)        
        phones    = object.person.phones.all()
        addresses = object.person.address.all()
        documents = object.person.document.all()
        emails    = object.person.emails.all()
        sites     = object.person.sites.all()
        instantMessengers = object.person.instantMessengers.all()
        last_update = object.history.latest('_audit_timestamp')._audit_timestamp
    except:        
        object= Employee()
        
    return render_to_response('employee/employee_form.html',
                              {'object': object, 'emails': emails, 'websites': sites, 'ims': instantMessengers, 'phones': phones, 'addresses': addresses, 'countries': Country.objects.all(), 'PhoneTypes': PhoneType.objects.all(), 'AddressTypes': AddressType.objects.all(), 'EmailTypes': EmailType.objects.all(), 'IMNetworks': IMNetwork.objects.all() , 'documents': documents, 'TypeDocuments': TypeDocument.objects.all(), 'Issuers': Issuer.objects.all(), 'States': State.objects.all(), 'MaritalStatusTypes': MaritalStatus.objects.all(), 'last_update': last_update },
                              context_instance=RequestContext(request)
                              )

def save(request, object_id= ''):
    """
    This function view saves an employees, its address and phones.
    @param request: this is a request sent by the browser.
    @type request: an instance of the class C{HttpRequest} created by the framework Django.
    @param object_id: it is the I{id} of the employee that must be saved.
    @type object_id: an instance of the built-in type C{int}. 
    """    
    try:
        object = get_object_or_404(Employee, pk=object_id)
        person = object.person
    except Http404:
        object = Employee()
        person = Person()
    
    object.person = person_save(request, person)
    object.job = request.POST['job']
    if(request.POST['hiredate']):
        object.hiredate = request.POST['hiredate']
    object.save()

    return HttpResponse(object.id)

def delete(request, object_id):
    """
    This function view search for an employee which has the id equals to the C{int} (I{employee_id})
    passed as parameter and change the field I{active} to "False' 
    @param request: this is a request sent by the browser.
    @type request: an instance of the class C{HttpRequest} created by the framework Django.
    @param object_id: represents the I{id} of the employee to be deleted.
    @type object_id: an instance of the built-in class C{int}.
    """
    object = get_object_or_404(Employee, pk=object_id)
    object.active = False
    object.save()
    return render_to_response('employee/employee_index.html', {'employeeList': Employee.objects.all().filter(active = True) })
