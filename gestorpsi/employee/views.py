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

from datetime import datetime
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.contrib import messages
from gestorpsi.employee.models import Employee
from gestorpsi.person.models import Person, MaritalStatus
from gestorpsi.phone.models import PhoneType
from gestorpsi.address.models import Country, State, AddressType, City
from gestorpsi.internet.models import EmailType, IMNetwork
from gestorpsi.document.models import TypeDocument, Issuer
from gestorpsi.person.views import person_save
from django.utils import simplejson
from gestorpsi.util.decorators import permission_required_with_403
from gestorpsi.person.views import person_json_list

@permission_required_with_403('employee.employee_list')
def index(request, deactive = False ):
    """
    This view function returns a list that contains all employees currently in the system.
    @param request: this is a request sent by the browser.
    @type request: a instance of the class C{HttpRequest} created by the framework Django
    """ 
    return render_to_response('employee/employee_list.html', locals(), context_instance=RequestContext(request))

def list(request, page = 1, initial = None, filter = None, no_paging = False, deactive = False ):
    user = request.user

    if deactive:
        object = Employee.objects.deactive(user.get_profile().org_active)
    else:   
        object = Employee.objects.active(user.get_profile().org_active)

    if initial:
        object = object.filter(person__name__istartswith = initial)
        
    if filter:
        object = object.filter(person__name__icontains = filter)

    return HttpResponse(simplejson.dumps(person_json_list(request, object, 'client.client_read', page, no_paging), sort_keys=True), mimetype='application/json')

@permission_required_with_403('employee.employee_list')
def lista(request, page = 1 , deactive = False):
    if deactive:
        object = Employee.objects.deactive(request.user.get_profile().org_active)
    else:   
        object = Employee.objects.active(request.user.get_profile().org_active)
         
    return HttpResponse(simplejson.dumps(person_json_list(request, object, 'employee.employee_read', page)),
                            mimetype='application/json')

@permission_required_with_403('employee.employee_write')
def form(request, object_id=None):
    """
    This function view creates an employee form. If the object_id has a value, this form will be fill with employee information.
    otherwise, a new form will be create
    @param request: this is a request sent by the browser.
    @type request: an instance of the class C{HttpRequest} created by the framework Django.
    @param object_id: it is the I{id} of the employee that must be saved.
    @type object_id: an instance of the built-in type C{int}. 
    """

    if object_id:
        object = get_object_or_404(Employee, pk=object_id, person__organization=request.user.get_profile().org_active)
    else:
        if not request.user.has_perm('employee.employee_write'):
            return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

        object = Employee()

    try:
        cities = City.objects.filter(state=request.user.get_profile().org_active.address.all()[0].city.state)
    except:
        cities = {}

    return render_to_response('employee/employee_form.html', {
                                'object': object,
                                'phones' : None if not hasattr(object, 'person') else object.person.phones.all(),
                                'addresses' : None if not hasattr(object, 'person') else object.person.address.all(),
                                'documents' : None if not hasattr(object, 'person') else object.person.document.all(),
                                'emails' : None if not hasattr(object, 'person') else object.person.emails.all(),
                                'websites' : None if not hasattr(object, 'person') else object.person.sites.all(),
                                'ims' : None if not hasattr(object, 'person') else object.person.instantMessengers.all(),
                                'countries': Country.objects.all(),
                                'PhoneTypes': PhoneType.objects.all(),
                                'AddressTypes': AddressType.objects.all(),
                                'EmailTypes': EmailType.objects.all(),
                                'IMNetworks': IMNetwork.objects.all() ,
                                'TypeDocuments': TypeDocument.objects.all(),
                                'Issuers': Issuer.objects.all(),
                                'States': State.objects.all(),
                                'MaritalStatusTypes': MaritalStatus.objects.all(),
                                'Cities': cities,
                              }, context_instance=RequestContext(request))

@permission_required_with_403('employee.employee_write')
def save(request, object_id=None):
    """
    This function view saves an employees, its address and phones.
    @param request: this is a request sent by the browser.
    @type request: an instance of the class C{HttpRequest} created by the framework Django.
    @param object_id: it is the I{id} of the employee that must be saved.
    @type object_id: an instance of the built-in type C{int}. 
    """    

    if object_id:
        object = get_object_or_404(Employee, pk=object_id, person__organization=request.user.get_profile().org_active)
        person = object.person
    else:
        object = Employee()
        person = Person()

    object.person = person_save(request, person)
    object.job = request.POST['job']
    if(request.POST['hiredate']):
        object.hiredate = datetime.strptime(request.POST['hiredate'],'%d/%m/%Y')

    object.save()

    messages.success(request, _('Employee saved successfully'))

    return HttpResponseRedirect('/employee/%s/' % object.id)

@permission_required_with_403('employee.employee_write')
def order(request, object_id=None):
    """
    This function view search for an employee which has the id equals to the C{int} (I{employee_id})
    passed as parameter and change the field I{active} to "False'
    @param request: this is a request sent by the browser.
    @type request: an instance of the class C{HttpRequest} created by the framework Django.
    @param object_id: represents the I{id} of the employee to be deleted.
    @type object_id: an instance of the built-in class C{int}.
    """
    object = get_object_or_404(Employee, pk=object_id, person__organization=request.user.get_profile().org_active)

    if (object.active == True):
        object.active = False
    else:
        object.active = True

    object.save(force_update=True)
    messages.success(request, ('%s' % (_('Employee activated successfully') if object.active else _('Employee deactivated successfully'))))
    return HttpResponseRedirect('/employee/%s/' % object.id)
