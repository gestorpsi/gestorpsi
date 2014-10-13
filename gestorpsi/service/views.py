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
from django.db.models import Q
from django.contrib import messages
from gestorpsi.service.models import Service, Area, ServiceType, Modality
from gestorpsi.person.views import person_json_list
from gestorpsi.careprofessional.models import CareProfessional, Profession
from gestorpsi.referral.models import Queue, Referral
from django.utils import simplejson
from gestorpsi.util.decorators import permission_required_with_403
from gestorpsi.util.views import get_object_or_None, color_rand
from gestorpsi.organization.models import AgeGroup, EducationLevel, HierarchicalLevel
from gestorpsi.careprofessional.models import CareProfessional, Profession
from gestorpsi.service.models import Service, Area, ServiceType, Modality, ServiceGroup
from gestorpsi.service.forms import ServiceGroupForm, GenericAreaForm, SchoolAreaForm, OrganizationalAreaForm, GENERIC_AREA #, ClinicAreaForm
from gestorpsi.client.forms import Client

def _can_view_group(request, group=None, service=None):
    """
    this method must to check if request user have perms to view group data
    both parameters can be used. at least one must be used
    """
    if request.user.groups.filter(name='administrator') or request.user.groups.filter(name='secretary'):
        return True

    if group and hasattr(request.user.profile.person, 'careprofessional'):
        # can view only professional responsible and professionals related
        if group:
            if request.user.profile.person.careprofessional in group.service.responsibles.all() or \
                request.user.profile.person.careprofessional in group.service.professionals.all():
                return True
        if service:
            if request.user.profile.person.careprofessional in service.responsibles.all() or \
                request.user.profile.person.careprofessional in service.professionals.all():
                return True 

    return False

def _can_write_group(request, service):
    if request.user.groups.filter(name='administrator') or request.user.groups.filter(name='secretary'):
        return True

    if hasattr(request.user.profile.person, 'careprofessional'):
        if request.user.profile.person.careprofessional in service.responsibles.all():
            return True

    return False

def _group_list(request, service = None):
    # filter only groups that request user have permission to read them clients
    if request.user.groups.filter(name='administrator') or request.user.groups.filter(name='secretary'):
        group_list = ServiceGroup.objects.filter(service=service).distinct()
    else:
        group_list = ServiceGroup.objects.filter(service=service, service__referral__client__id__in = [i.id for i in _service_clients(request, service)]).distinct()

    return group_list

def _queue_list(request, service):
    queue_list = Queue.objects.filter(referral__service__organization=request.user.get_profile().org_active, \
        referral__service=service, \
        date_in__isnull = False, date_out__isnull = True, \
        referral__client__in = [s for s in _service_clients(request, service) ]) \
        .order_by('priority','date_in','referral__client__person__name') \
        .distinct()
    return queue_list

@permission_required_with_403('service.service_list')
def index(request, deactive = False):
    """
    Returns a list that contains all the currently existing services.
    @param request: this is a request sent by the browser.
    @type request: an instance of the class C{HttpRequest} created by the framework Django.
    """
    return render_to_response( "service/service_list.html", locals(), context_instance=RequestContext(request))

@permission_required_with_403('service.service_list')
def list(request, page = 1, initial = None, filter = None, no_paging = False, deactive = False):
    if deactive:
        object = Service.objects.filter( active=False, organization=request.user.get_profile().org_active )
    else:
        object = Service.objects.filter( active=True, organization=request.user.get_profile().org_active )
        
    if initial:
        object = object.filter(name__istartswith = initial)
        
    if filter:
        object = object.filter(Q(name__icontains = filter) | Q(referral__client__person__name__icontains=filter)).distinct()

    object_length = len(object)
    paginator = Paginator(object, settings.PAGE_RESULTS)
    object = paginator.page(page)

    array = {} #json
    i = 0

    array['util'] = {
        'has_perm_read': request.user.has_perm('service.service_read'),
        'paginator_has_previous': object.has_previous().real,
        'paginator_has_next': object.has_next().real,
        'paginator_previous_page_number': object.previous_page_number().real,
        'paginator_next_page_number': object.next_page_number().real,
        'paginator_actual_page': object.number,
        'paginator_num_pages': paginator.num_pages,
        'object_length': object_length,
        'is_student': True if hasattr(request.user.profile.person, 'careprofessional') and request.user.profile.person.careprofessional.is_student else False,
    }

    array['paginator'] = {}
    for p in paginator.page_range:
        array['paginator'][p] = p

    for o in object.object_list:
        # can add group only with service_write or professional is responsible for service
        name = u'%s' % o.name
        if o.is_group:
            name += " (%s)" % _('Group')
        array[i] = {
            'id': o.id,
            'name': o.name_html,
            'is_group': False if not o.is_group else True,
            'description': u'%s' % o.description,
            'email': '',
            #'have_client_to_list': False if not len(_group_list(request, o)) else True,
            'have_client_to_list': True,
            'can_add_group': False if not _can_write_group(request, o) else True,
        }
        i = i + 1

    return HttpResponse(simplejson.dumps(array, sort_keys=True), mimetype='application/json')

@permission_required_with_403('service.service_write')
def select_area(request, object_id=''):
    object = get_object_or_404(Service, pk=object_id, organization=request.user.get_profile().org_active) if object_id else Service()
    return render_to_response('service/select_area.html', {
                                        'areas': Area.objects.all(),
                                        'object': object, },
                                        context_instance=RequestContext(request) )

@permission_required_with_403('service.service_read')
def form(request, object_id=None):
    object = get_object_or_404(Service, pk=object_id, organization=request.user.get_profile().org_active) if object_id else Service()
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

    # select a next color when new register
    if not object.pk:
        object.color = color_rand()
        #if not request.user.get_profile().org_active.service_set.all():
            #object.css_color_class = 1
        #else:
            #if not object.css_color_class:
                #object.css_color_class = (int(Service.objects.filter(organization=request.user.get_profile().org_active).latest('date').css_color_class) + 1) \
                                    #if int(Service.objects.filter(organization=request.user.get_profile().org_active).latest('date').css_color_class) <=24 \
                                    #else 1

    return render_to_response('service/service_form.html', {
        'object': object,
        'CareProfessionals': CareProfessional.objects.active(request.user.get_profile().org_active),
        'Students': CareProfessional.objects.students_active(request.user.get_profile().org_active),
        'AgeGroups': AgeGroup.objects.all(),
        'Areas': Area.objects.all(),
        'ServiceTypes': ServiceType.objects.all(),
        'Modalitys': Modality.objects.all(),
        'Professions': Profession.objects.all(),
        'area': selected_area,
        'form_area': form_area,
        'clss':request.GET.get('clss'),
        'client_list': _service_clients(request, object),
        'queue_list': _queue_list(request,object),
        'can_list_groups': False if not len(_group_list(request, object)) else True,
        'can_write_group': False if not _can_write_group(request, object) else True,
        }, context_instance=RequestContext(request) )

@permission_required_with_403('service.service_write')
def save(request, object_id=''):

    object = get_object_or_404(Service, pk=object_id, organization=request.user.get_profile().org_active) if object_id else Service()
    object.organization = request.user.get_profile().org_active
    object.name = request.POST.get('service_name')
    object.description = request.POST.get('service_description')
    object.keywords = request.POST.get('service_keywords')
    object.comments = request.POST.get('comments')
    object.academic_related = request.POST.get('academic_related') or False
    object.is_group = request.POST.get('is_group') or False
    object.is_online = request.POST.get('is_online') or False
    object.service_type = ServiceType.objects.get(pk=request.POST.get('service_type'))

    if not object_id:
        object.research_project = request.POST.get('research_project') or False
        object.research_project_name = request.POST.get('research_project_name')
        object.area = Area.objects.get(pk=request.POST.get('service_area'))
    else:
        object.css_color_class = request.POST.get('service_css_color_class')
    
    object.color = request.POST.get('service_color')
    object.save() # save object

    """ Responsibles list """
    object.responsibles.clear()
    for p in request.POST.getlist('service_responsibles'):
        object.responsibles.add(CareProfessional.objects.get(pk=p))

    """ Professions """
    object.professions.clear()
    for p in request.POST.getlist('service_profession'):
        object.professions.add(Profession.objects.get(pk=p))

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

    """ Professionals list """
    object.professionals.clear()
    for p in request.POST.getlist('service_professionals'):
        object.professionals.add(CareProfessional.objects.get(pk=p))

    object.save()
    messages.success(request, _('Service saved successfully'))

    return HttpResponseRedirect('/service/form/%s/' % object.id)

@permission_required_with_403('service.service_list')
def list_professional(request, object_id):
    """ Referral - List of professional of the service """

    list_prof = CareProfessional.objects.filter(prof_services = object_id, person__organization=request.user.get_profile().org_active)
    i = 0
    array = {} #JSON
    for o in list_prof:
        name = o if not o.is_student else u'%s (%s)' % (o, _('Student'))
        array[i] = {
                'name': '%s' % name,
                'id': o.id,
        }
        i = i + 1

    return HttpResponse(simplejson.dumps(array), mimetype='application/json')

@permission_required_with_403('service.service_write')
def order(request, object_id=None):
    object = get_object_or_404(Service, pk=object_id, organization=request.user.get_profile().org_active)
    url = "/service/form/%s/"

    """ CHECK QUEUE AND REFERRAL """
    if ( Referral.objects.charged().filter(service = object).count()) == 0:
        if (Queue.objects.filter(referral__service = object_id, date_out = None).order_by('date_in').order_by('priority').count()) == 0:
            if object.active == True:
                messages.success(request, _('Service deactive successfully'))
                object.active = False
            else:
                messages.success(request, _('Service active successfully'))
                object.active = True

            object.save(force_update = True)
        else:
            messages.success(request, _('You can not disable a service with clients in the queue'))
            url += '?clss=error'
    else:
            messages.success(request, _('You can not disable a service with clients registered in the referral'))
            url += '?clss=error'
    return HttpResponseRedirect(url % object.id)

@permission_required_with_403('service.service_write')
def disable(request, object_id=None):
    """
    This function view searches for a C{Service} object which has the id equals to I{object_id}, if there is
    such C{Service} instance it is disabled.
    """
    object = get_object_or_404(Service, pk=object_id, organization=request.user.get_profile().org_active)
    object.active = False
    object.save()
    return render_to_response( "service/service_index.html", {
        'object':Service.objects.filter( active=True, organization=request.user.get_profile().org_active ),
        'CareProfessionals': CareProfessional.objects.all(person__organization = request.user.get_profile().org_active.id),
        'AgeGroups': AgeGroup.objects.all(),
        'Areas': Area.objects.all(),
        'ServiceTypes': ServiceType.objects.all(),
        'Modalitys': Modality.objects.all(),
        'Professions': Profession.objects.all(),
        }, context_instance=RequestContext(request))


@permission_required_with_403('service.service_list')
def queue(request, object_id=None):
    object = get_object_or_404(Service, pk=object_id, organization=request.user.get_profile().org_active)

    return render_to_response( "service/service_queue.html", {
        'queue_list': _queue_list(request, object),
        'object': object,
        'client_list': _service_clients(request, object),
        }, context_instance=RequestContext(request))

def _service_clients(request, service):
    # select clients by service and organization
    client_list = Client.objects.filter(person__organization = request.user.get_profile().org_active.id, referral__service=service, referral__referraldischarge__isnull=True).distinct()

    # check if user have at least one referral charged on selected service
    is_client_charged = []
    for i in client_list:
        if i.id not in is_client_charged and i.referrals_charged():
            is_client_charged.append(i.id)
    client_list = client_list.filter(pk__in = is_client_charged)
    
    if not request.user.groups.filter(name='administrator') and not request.user.groups.filter(name='secretary'):
        client_list = client_list.filter(Q(referral__professional = request.user.profile.person.careprofessional.id) \
                        | Q(person__user__id=request.user.id) \
                        | Q(referral__service__responsibles=request.user.profile.person.careprofessional) \
                        ).distinct().order_by('-active', 'person__name')

    return client_list

@permission_required_with_403('client.client_list')
def client_list_index(request, object_id = None):
    # deny access to student add new referral
    if hasattr(request.user.profile.person, 'careprofessional') and request.user.profile.person.careprofessional.is_student:
        return render_to_response('403.html', {'object': _("Sorry! Students have no access to this service!"), }, context_instance=RequestContext(request))

    object = get_object_or_404(Service, pk=object_id, organization=request.user.get_profile().org_active)

    client_list = _service_clients(request, object)
    queue_list = _queue_list(request, object)

    return render_to_response('service/service_client_list.html', locals(), context_instance=RequestContext(request))

# list referral groups
@permission_required_with_403('service.service_list')
def group_list(request, object_id=None, return_json=False):
    service = get_object_or_404(Service, pk=object_id, organization = request.user.get_profile().org_active)
    object = _group_list(request, service)

    if hasattr(request.user.profile.person, 'careprofessional') and request.user.profile.person.careprofessional.is_student:
        return render_to_response('403.html', {'object': _("Sorry! Students have no access to this service!"), }, context_instance=RequestContext(request))

    if return_json:
        i = 0
        array = {} #JSON
        for o in object:
            array[i] = {
                    'name': '%s' % o.description,
                    'id': o.id,
            }
            i = i + 1

        return HttpResponse(simplejson.dumps(array), mimetype='application/json')

    return render_to_response('service/service_group_list.html',
                              { 'object': object, 
                               'service': Service.objects.get(pk=object_id),
                               'queue_list': _queue_list(request, service),
                               'client_list': _service_clients(request, service),
                              },
                              context_instance=RequestContext(request)
                              )

# NOTE: Permission below must to been checked by _can_manage_group method
#@permission_required_with_403('service.service_write')
def group_form(request, object_id=None, group_id=None):
    object = get_object_or_404(Service, pk=object_id, organization = request.user.get_profile().org_active)
    
    if not object.is_group:
        return render_to_response('403.html', {'object':_('Sorry, this service was configured without group support.')})
    
    if not object.active:
        return render_to_response('403.html', {'object':_('Sorry, this you can not add groups in disabled services.')})

    group = get_object_or_None(ServiceGroup, pk=group_id, service__organization = request.user.get_profile().org_active)

    if request.method == 'POST':
        if not _can_write_group(request, object):
            return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))
        
        form = ServiceGroupForm(request.POST, instance=group) if group else ServiceGroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.service = object 
            group.save()
            messages.success(request, _('Group saved successfully'))
            return HttpResponseRedirect('/service/%s/group/%s/form/' % (object.id, group.id))

    else:
        if not group: # adding new. only if have write permission on this service
            if not _can_write_group(request, object):
                return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))
        
        else: # opening existing group
            if not _can_view_group(request, group):
                return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

        form = ServiceGroupForm(instance=group) if group else ServiceGroupForm()

    return render_to_response('service/service_group_form.html',
                              {'object': object, 
                                'form': form,
                                'group': group,
                                'queue_list': _queue_list(request, object),
                                'client_list': _service_clients(request, object),
                                'hide_service_actions': True,
                                'have_write_perms': False if not _can_write_group(request, object) else True,
                               },
                              context_instance=RequestContext(request)
                              )

