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

from django.utils import simplejson
from django.utils.translation import ugettext as _
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.template import RequestContext
from django.utils.translation import ugettext as _
from gestorpsi.service.models import Service, Area, ServiceType, Modality
from gestorpsi.organization.models import Agreement, AgeGroup, ProcedureProvider, Procedure
from gestorpsi.careprofessional.models import CareProfessional, Profession
from gestorpsi.referral.models import Queue, Referral
from django.utils import simplejson
from gestorpsi.util.decorators import permission_required_with_403
from gestorpsi.util.views import get_object_or_None
from gestorpsi.organization.models import Agreement, AgeGroup, EducationLevel, HierarchicalLevel
from gestorpsi.careprofessional.models import CareProfessional, Profession
from gestorpsi.service.models import Service, Area, ServiceType, Modality
from gestorpsi.service.forms import GenericAreaForm, SchoolAreaForm, OrganizationalAreaForm, GENERIC_AREA #, ClinicAreaForm

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

def select_area(request, object_id=''):
    object = get_object_or_None(Service, pk=object_id) or Service()
    return render_to_response('service/select_area.html', {
                                        'areas': Area.objects.all(),
                                        'object': object, },
                                        context_instance=RequestContext(request) )

def form(request, object_id=''):
    object = get_object_or_None(Service, pk=object_id) or Service()
    selected_area = get_object_or_None(Area, area_code=request.POST.get('area')) or object.area

    if selected_area.area_code in GENERIC_AREA:
        form_area = GenericAreaForm(instance=object)
        form_area.fields['age_group'].queryset = selected_area.age_group.all()

    if selected_area.area_code in ('school', 'psychoedu'):
        form_area = SchoolAreaForm(instance=object)
        form_area.fields['education_level'].queryset = selected_area.education_level.all()

    if selected_area.area_code == 'organizational':
        form_area = OrganizationalAreaForm(instance=object)
        form_area.fields['hierarchical_level'].queryset = selected_area.hierarchical_level.all()

    form_area.fields['service_type'].queryset = selected_area.service_type.all()
    form_area.fields['modalities'].queryset = selected_area.modalities.all()

    return render_to_response('service/service_form.html', {
        'object': object,
        'Agreements': Agreement.objects.all(),
        'CareProfessionals': CareProfessional.objects.filter(person__organization= request.user.get_profile().org_active),
        'AgeGroups': AgeGroup.objects.all(),
        'Areas': Area.objects.all(),
        'ServiceTypes': ServiceType.objects.all(),
        'Modalitys': Modality.objects.all(),
        'Professions': Profession.objects.all(),
        'area': selected_area,
        'form_area': form_area,},
        context_instance=RequestContext(request) )

@permission_required_with_403('service.service_write')
def save(request, object_id=''):
    object = get_object_or_None(Service, pk=object_id) or Service()
    object.organization = request.user.get_profile().org_active
    object.name = request.POST.get('service_name')
    object.description = request.POST.get('service_description')
    object.keywords = request.POST.get('service_keywords')
    object.research_project = request.POST.get('research_project') or False
    object.research_project_name = request.POST.get('research_project_name')
    object.comments = request.POST.get('comments')

    """ chose one css color to this service """
    if not (object.css_color_class):
        try:
            latest_css = Service.objects.filter(organization=request.user.get_profile().org_active).latest('date')
            next_css = latest_css.css_color_class + 1
            if next_css <= 24:
                object.css_color_class = next_css
            else:
                object.css_color_class = 1
        except:
            pass

    object.area =  Area.objects.get(pk=request.POST.get('service_area'))
    object.service_type = ServiceType.objects.get(pk=request.POST.get('service_type'))
    object.save()

    """ Professions """
    object.professions.clear()
    for p in request.POST.getlist('service_profession'):
        object.professions.add(Profession.objects.get(pk=p))

    """ Agreements """
    object.agreements.clear()
    for a in request.POST.getlist('service_agreements'):
        object.agreements.add(Agreement.objects.get(pk=a))

    """ Professionals list """
    object.professionals.clear()
    for p in request.POST.getlist('service_professionals'):
        object.professionals.add(CareProfessional.objects.get(pk=p))

    """ Responsibles list """
    object.responsibles.clear()
    for p in request.POST.getlist('service_responsibles'):
        object.responsibles.add(CareProfessional.objects.get(pk=p))

    """ Modalities """
    object.modalities.clear()
    for m in request.POST.getlist('modalities'):
        object.modalities.add(Modality.objects.get(pk=m))

    """ Age Group """
    object.age_group.clear()
    for age in request.POST.getlist('age_group'):
        object.age_group.add(AgeGroup.objects.get(pk=age))

    """ Education Level """
    object.education_level.clear()
    for edu in request.POST.getlist('education_level'):
        object.education_level.add(EducationLevel.objects.get(pk=edu))

    """ Hierachical Level """
    object.hierarchical_level.clear()
    for hierarc in request.POST.getlist('hierarchical_level'):
        object.hierarchical_level.add(HierarchicalLevel.objects.get(pk=hierarc))

    request.user.message_set.create(message=_('Service saved successfully'))

    return HttpResponseRedirect('/service/form/%s/' % object.id)

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

@permission_required_with_403('service.service_write')
def queue(request, object_id = ''):
    object = Service.objects.get(pk = object_id)

    queue = Queue.objects.filter(referral__service = object_id, date_out = None).order_by('date_in').order_by('priority')

    list_queue = Referral.objects.filter(queue__referral__service = object_id, queue__date_out = None).order_by('date').order_by('-priority')

    return render_to_response( "service/service_queue.html", {
        'queues': list_queue,
        'object': object,
        }, context_instance=RequestContext(request))
