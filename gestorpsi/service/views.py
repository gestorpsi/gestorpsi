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
from django.http import HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from gestorpsi.service.models import Service, Area, ServiceType, Modality, AreaClinic
from gestorpsi.organization.models import Agreement, AgeGroup, ProcedureProvider, Procedure, Organization
from gestorpsi.careprofessional.models import CareProfessional, Profession 

def index(request):
    """
    Returns a list that contains all the currently existing services.
    @param request: this is a request sent by the browser.
    @type request: an instance of the class C{HttpRequest} created by the framework Django.
    """
    user = request.user
    
    return render_to_response( "service/service_index.html", {
        'object':Service.objects.filter( active=True, organization=user.org_active ),
        'Agreements': Agreement.objects.all(),
        'CareProfessionals': CareProfessional.objects.filter(person__organization=user.org_active),
        'AgeGroups': AgeGroup.objects.all(),
        'ProcedureProviders': ProcedureProvider.objects.all(),
        'Procedures': Procedure.objects.all(),
        'Areas': Area.objects.all(),
        'ServiceTypes': ServiceType.objects.all(),
        'Modalitys': Modality.objects.all(),
        'Professions': Profession.objects.all(),
        })

def form(request, object_id=''):
    """
    This function view uses I{forms} to show the information related to the
    C{Service} with id equals to I{object_id}
    @param request: this is a request sent by the browser.
    @type request: an instance of the class C{HttpRequest} created by the framework Django.
    @param object_id: id of the C{Service}.
    @type object_id: an instance of the built-in class I{int}.
    """
    try:
        object= get_object_or_404( Service, pk= object_id )
    except (Http404, ObjectDoesNotExist):
        object= Service()
    
    return render_to_response('service/service_form.html', {
        'object': object,
        'Agreements': Agreement.objects.all(),
        'CareProfessionals': CareProfessional.objects.all(),
        'AgeGroups': AgeGroup.objects.all(),
        'ProcedureProviders': ProcedureProvider.objects.all(),
        'Procedures': Procedure.objects.all(),
        'Areas': Area.objects.all(),
        'ServiceTypes': ServiceType.objects.all(),
        'Modalitys': Modality.objects.all(),
        'Professions': Profession.objects.all(),
        } )

def save_clinic(request, object):
    ac = AreaClinic()
    ac.save()
    ac.age_group.clear()
    for age in request.POST.getlist('service_age'):
        ac.age_group.add(AgeGroup.objects.get(pk=age))
    object.content_object = ac
    object.save()
    return object

# Follow the model
#def save_whatever():
#    do a lot of things here
#    return the 'object' saved

def save(request, object_id = ''):
    """
    This function view searches for the C{Service} with id equals to I{object_id}, if there is such a
    C{Service} instance, it is loaded and updated with the values of the request object, otherwise a 
    new C{Service} instance is created, filled with request's values and saved.
    """

    try:
        object = get_object_or_404(Service, pk=object_id)
    except:
        user = request.user
        object = Service()
        object.organization = user.org_active
    
    object.name = request.POST['service_name']
    object.description = request.POST['service_description']
    object.keywords = request.POST['service_keywords']
    if request.POST['service_active'] == 'True':
        object.active = True
    else:
        object.active = False
    object.area = Area.objects.get(pk=request.POST['service_area'])
    object.service_type = ServiceType.objects.get(pk=request.POST['service_type'])
    object.research_project = request.POST['research_project']
    
    object.save()

    """ Modalities """
    object.modalities.clear()
    for m in request.POST.getlist('service_solicitation'):
        object.modalities.add(Modality.objects.get(pk=m))

    """ Procedures """
    object.procedures.clear()
    for p in request.POST.getlist('service_type_procedure'):
        object.procedures.add(Procedure.objects.get(pk=p))
    
    """ Agreements """
    object.agreements.clear()
    for a in request.POST.getlist('service_agreements'):
        object.agreements.add(Agreement.objects.get(pk=a))
    
    """ Professions """
    object.professions.clear()
    for p in request.POST.getlist('service_profession'):
        object.professions.add(Profession.objects.get(pk=p))

    """ Lista de Profissionais """
    object.professionals.clear()
    for p in request.POST.getlist('service_professionals'):
        object.professionals.add(CareProfessional.objects.get(pk=p))

    """ Lista de Responsaveis """
    object.responsibles.clear()
    for p in request.POST.getlist('service_responsibles'):
        object.responsibles.add(CareProfessional.objects.get(pk=p))


    """ Clinic Area """
    if request.POST['service_area'] == '3':
        object = save_clinic(request, object)

    return HttpResponse(object.id)

def disable(request, object_id=''):
    """
    This function view searches for a C{Service} object which has the id equals to I{object_id}, if there is
    such C{Service} instance it is disabled.
    """
    user = request.user
    object = get_object_or_404( Service, pk=object_id )
    object.active = False
    object.save()
    return render_to_response( "service/service_index.html", {
        'object':Service.objects.filter( active=True, organization=user.org_active ),
        'Agreements': Agreement.objects.all(),
        'CareProfessionals': CareProfessional.objects.all(person__organization = user.org_active.id),
        'AgeGroups': AgeGroup.objects.all(),
        'ProcedureProviders': ProcedureProvider.objects.all(),
        'Procedures': Procedure.objects.all(),
        'Areas': Area.objects.all(),
        'ServiceTypes': ServiceType.objects.all(),
        'Modalitys': Modality.objects.all(),
        'Professions': Profession.objects.all(),
        })