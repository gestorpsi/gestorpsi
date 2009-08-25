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

from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.utils.translation import ugettext as _
from gestorpsi.service.models import Service, Area, ServiceType, Modality, AreaClinic
from gestorpsi.organization.models import Agreement, AgeGroup, ProcedureProvider, Procedure
from gestorpsi.careprofessional.models import CareProfessional, Profession
from gestorpsi.referral.models import Queue
from django.utils import simplejson
from gestorpsi.util.decorators import permission_required_with_403
from django.core.paginator import Paginator

@permission_required_with_403('service.service_list')
def index(request):
    """
    Returns a list that contains all the currently existing services.
    @param request: this is a request sent by the browser.
    @type request: an instance of the class C{HttpRequest} created by the framework Django.
    """
    return render_to_response( "service/service_list.html", context_instance=RequestContext(request))

@permission_required_with_403('service.service_list')
def list(request, page = 1):
    user = request.user
    object = Service.objects.filter( active=True, organization=user.get_profile().org_active )
    
    object_length = len(object)
    paginator = Paginator(object, settings.PAGE_RESULTS)
    object = paginator.page(page)

    array = {} #json
    i = 0

    array['util'] = {
        'has_perm_read': user.has_perm('service.service_read'),
        'paginator_has_previous': object.has_previous().real,
        'paginator_has_next': object.has_next().real,
        'paginator_previous_page_number': object.previous_page_number().real,
        'paginator_next_page_number': object.next_page_number().real,
        'paginator_actual_page': object.number,
        'paginator_num_pages': paginator.num_pages,
        'object_length': object_length,
    }

    array['paginator'] = {}
    for p in paginator.page_range:
        array['paginator'][p] = p
    
    for o in object.object_list:
        array[i] = {
            'id': o.id,
            'name': u'%s' % o.name,
            'description': u'%s' % o.description,
            'email': '',
        }
        i = i + 1

    return HttpResponse(simplejson.dumps(array), mimetype='application/json')

@permission_required_with_403('service.service_read')
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
        'CareProfessionals': CareProfessional.objects.filter(person__organization= request.user.get_profile().org_active),
        'AgeGroups': AgeGroup.objects.all(),
        'ProcedureProviders': ProcedureProvider.objects.all(),
        'Procedures': Procedure.objects.all(),
        'Areas': Area.objects.all(),
        'ServiceTypes': ServiceType.objects.all(),
        'Modalitys': Modality.objects.all(),
        'Professions': Profession.objects.all(),},
        context_instance=RequestContext(request) )

@permission_required_with_403('service.service_write')
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

@permission_required_with_403('service.service_write')
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
        object.organization = user.get_profile().org_active
    
    object.name = request.POST['service_name']
    object.description = request.POST['service_description']
    object.keywords = request.POST['service_keywords']
    object.comments = request.POST.get('comments')
    object.area = Area.objects.get(pk=request.POST['service_area'])
    object.service_type = ServiceType.objects.get(pk=request.POST['service_type'])
    object.research_project_name = request.POST.get('research_project_name')
    try:
        object.research_project = request.POST['research_project']
    except:
        object.research_project = False
    
    """ chose one css color to this service """
    if not (object.css_color_class):
        try:
            user = request.user
            latest_css = Service.objects.filter(organization=user.get_profile().org_active).latest('date')
            next_css = latest_css.css_color_class + 1
            if next_css <= 24:
                object.css_color_class = next_css
            else:
                object.css_color_class = 1
    
        except:
            pass

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

    request.user.message_set.create(message=_('Service saved successfully'))

    return HttpResponseRedirect('/service/%s/' % object.id)

@permission_required_with_403('service.service_write')
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
        'object':Service.objects.filter( active=True, organization=user.get_profile().org_active ),
        'Agreements': Agreement.objects.all(),
        'CareProfessionals': CareProfessional.objects.all(person__organization = user.get_profile().org_active.id),
        'AgeGroups': AgeGroup.objects.all(),
        'ProcedureProviders': ProcedureProvider.objects.all(),
        'Procedures': Procedure.objects.all(),
        'Areas': Area.objects.all(),
        'ServiceTypes': ServiceType.objects.all(),
        'Modalitys': Modality.objects.all(),
        'Professions': Profession.objects.all(),
        }, context_instance=RequestContext(request))


@permission_required_with_403('service.service_list')
def list_professional(request, object_id):
    """ Referral - List of professional of the service """
    try:
        list_prof = CareProfessional.objects.filter(prof_services = object_id)
        
        i = 0
        array = {} #JSON

        for o in list_prof:
            array[i] = {
                    'name': '%s' % o,
                    'id': o.id,
            }
            i = i + 1
        
        return HttpResponse(simplejson.dumps(array), mimetype='application/json')

    except:
        pass

@permission_required_with_403('service.service_write')
def order(request, object_id = ''):
    object = Service.objects.get(pk = object_id)

    if object.active == True:
       object.active = False
    else:
        object.active = True

    object.save(force_update = True)
    return HttpResponseRedirect('/service/%s/' % object.id)


@permission_required_with_403('service.service_write')
def queue(request, object_id = ''):
    object = Service.objects.get(pk = object_id)

    list_queue = Queue.objects.filter(referral__service = object_id, date_out = None).order_by('date_in').order_by('priority')

    return render_to_response( "service/service_queue.html", {
        'queues': list_queue,
        'object': object,
        }, context_instance=RequestContext(request))
