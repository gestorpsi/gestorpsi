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
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.utils.translation import ugettext as _
from gestorpsi.person.models import Person, MaritalStatus
from gestorpsi.person.views import person_json_list, person_save
from gestorpsi.careprofessional.models import ProfessionalProfile, ProfessionalIdentification, CareProfessional, Profession
from gestorpsi.organization.models import Agreement
from gestorpsi.phone.models import PhoneType
from gestorpsi.address.models import Country, State, AddressType, City
from gestorpsi.internet.models import EmailType, IMNetwork
from gestorpsi.document.models import TypeDocument, Issuer
from gestorpsi.place.models import Place, PlaceType
from gestorpsi.service.models import Service
from gestorpsi.referral.models import Referral
from gestorpsi.util.decorators import permission_required_with_403
from gestorpsi.util.views import get_object_or_None
from gestorpsi.authentication.models import Profile, Role
from gestorpsi.careprofessional.forms import StudentProfileForm
from django.contrib.auth.models import User, Group
from django.contrib import messages

@permission_required_with_403('careprofessional.careprofessional_list')
def index(request, template_name='careprofessional/careprofessional_list.html', deactive = False):
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
  
@permission_required_with_403('careprofessional.careprofessional_list')
def list(request, page = 1, deactive = False, filter = None, initial = None, no_paging = False, is_student = False ):
    if not is_student: # professional
        if deactive:
            object = CareProfessional.objects.deactive(request.user.get_profile().org_active)
        else:
            object = CareProfessional.objects.active(request.user.get_profile().org_active)
    else: # stundent
        if deactive:
            object = CareProfessional.objects.students_deactive(request.user.get_profile().org_active)
        else:
            object = CareProfessional.objects.students_active(request.user.get_profile().org_active)

    if initial:
        object = object.filter(person__name__istartswith = initial)

    if filter:
        object = object.filter(person__name__icontains = filter)

    return HttpResponse(simplejson.dumps(person_json_list(request, object, 'careprofessional.careprofessional_read', page), sort_keys=True), mimetype='application/json')

@permission_required_with_403('careprofessional.careprofessional_read')
def form(request, object_id=None, template_name='careprofessional/careprofessional_form.html', is_student = False):
    if object_id:
        object = get_object_or_404(CareProfessional, pk=object_id, person__organization=request.user.get_profile().org_active)
    else:
        if not request.user.has_perm('careprofessional.careprofessional_write'):
            return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

        object = CareProfessional()

    try:
        cities = City.objects.filter(state=request.user.get_profile().org_active.address.all()[0].city.state)
    except:
        cities = {}

    if is_student:
        student_form = StudentProfileForm(instance=object.studentprofile) if object_id else StudentProfileForm()
        ServiceTypes = Service.objects.filter( active=True, organization=request.user.get_profile().org_active, academic_related=True )
    else:
        ServiceTypes = Service.objects.filter( active=True, organization=request.user.get_profile().org_active)
    

    return render_to_response(template_name, {
                                    'clss':request.GET.get('clss'),
                                    'object': object,
                                    'student_form': student_form if is_student else None,
                                    'phones' : None if not hasattr(object, 'person') else object.person.phones.all(),
                                    'addresses' : None if not hasattr(object, 'person') else object.person.address.all(),
                                    'documents' : None if not hasattr(object, 'person') else object.person.document.all(),
                                    'emails' : None if not hasattr(object, 'person') else object.person.emails.all(),
                                    'websites' : None if not hasattr(object, 'person') else object.person.sites.all(),
                                    'ims' : None if not hasattr(object, 'person') else object.person.instantMessengers.all(),
                                    'PROFESSIONAL_AREAS': Profession.objects.all(),
                                    'AgreementTypes': Agreement.objects.all(),
                                    'WorkPlacesTypes': Place.objects.active().filter(organization = request.user.get_profile().org_active.id),
                                    'countries': Country.objects.all(),
                                    'PhoneTypes': PhoneType.objects.all(),
                                    'AddressTypes': AddressType.objects.all(),
                                    'EmailTypes': EmailType.objects.all(),
                                    'IMNetworks': IMNetwork.objects.all() ,
                                    'TypeDocuments': TypeDocument.objects.all(),
                                    'Issuers': Issuer.objects.all(),
                                    'States': State.objects.all(),
                                    'MaritalStatusTypes': MaritalStatus.objects.all(),
                                    'PlaceTypes': PlaceType.objects.all(),
                                    'ServiceTypes': ServiceTypes,
                                    'Cities': cities,
                                    },
                              context_instance=RequestContext(request)
                              )

@permission_required_with_403('careprofessional.careprofessional_write')
def save_careprof(request, object_id, save_person, is_student=False):
    """
    This view function returns the informations about CareProfessional 
    @param request: this is a request sent by the browser.
    @type request: a instance of the class C{HttpRequest} created by the framework Django
    @param object: it is the tyoe of CareProfessional that must be filled.
    @type object: an instance of the built-in type C{CareProfessional}.            
    """
    if object_id:
        object = get_object_or_404(CareProfessional, pk=object_id, person__organization=request.user.get_profile().org_active)
    else:
        object = CareProfessional()

    if save_person:
        object.person = person_save(request, get_object_or_None(Person, pk=object.person_id) or Person())
    object.save()

    exist_referral="False"
    list_from_form = request.POST.getlist('professional_service')

    # MAKE A LIST WHIT ID SERVICE
    list_db = []
    for y in object.prof_services.filter(organization=request.user.get_profile().org_active):
        list_db.append(y.id)

    # IF LIST_FROM_FORM > 0 THEN ADDED SERVICE 
    if len(list_from_form) > 0:
        for ps_id in list_from_form:
            ps = Service.objects.get(pk=ps_id)
            object.prof_services.add(ps)

    # COMPARES THE LIST_DB AND LIST_FORM, THE RESULT WILL BE SERVICES THAT WILL BE REMOVED
    if len(list_from_form) > 0:
        for x in list_from_form:
            try:
                indice = list_db.remove(x)
            except:
                pass

    # REMOVE SERVICE 
    if len(list_db) > 0:
        for o in list_db:
            if Referral.objects.charged().filter(professional = object, service = o, status = '01').count() > 0:
                exist_referral="True"
            else:
                object.prof_services.remove(o)

    profile = get_object_or_None(ProfessionalProfile, pk=object.professionalProfile_id) or ProfessionalProfile()
    profile.initialProfessionalActivities = request.POST.get('professional_initialActivitiesDate')
    profile.save()
    object.professionalProfile = profile

    if (len(request.POST.getlist('professional_workplace'))):
        for o in profile.workplace.filter(organization=request.user.get_profile().org_active):
            profile.workplace.remove(o)
        for wplace_id in request.POST.getlist('professional_workplace'):
            profile.workplace.add(Place.objects.get(pk=wplace_id))

    if not is_student:
        if (len(request.POST.getlist('professional_agreement'))):
            profile.agreement.clear()
            for agreemt_id in request.POST.getlist('professional_agreement'):
                profile.agreement.add(Agreement.objects.get(pk=agreemt_id))

        if request.POST.get('professional_registerNumber') or request.POST.get('professional_area'):
            if not object.professionalIdentification:
                identification = ProfessionalIdentification()
            else:
                identification = object.professionalIdentification

            if request.POST.get('professional_registerNumber'):
                identification.registerNumber = request.POST.get('professional_registerNumber')

            if request.POST.get('professional_area'):
                identification.profession = get_object_or_None(Profession, id=request.POST.get('professional_area'))

            identification.save()
            object.professionalIdentification = identification

    object.save()
    return (object, exist_referral)

@permission_required_with_403('careprofessional.careprofessional_write')
def save(request, object_id=None, save_person=True, is_student=False):
    
    if is_student: # verify if student can join in service
        for ps in request.POST.getlist('professional_service'):
            if not Service.objects.filter(active=True, organization=request.user.get_profile().org_active, academic_related=True, pk=ps):
                return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    object = save_careprof(request, object_id, save_person, is_student)
    clss = request.GET.get('clss')
    exist_referral = object[1]
    object = object[0]
    if is_student:
        student_form = StudentProfileForm(request.POST, instance=object.studentprofile) if object_id else StudentProfileForm(request.POST)
        if student_form.is_valid():
            data = student_form.save(commit=False)
            data.professional = object
            data.save()

    if exist_referral == "False":
        request.user.message_set.create(message=_('Professional saved successfully') if not is_student else _('Student saved successfully'))
        return HttpResponseRedirect(('/careprofessional/%s/' % object.id) if not is_student else ('/careprofessional/student/%s/' % object.id))
    else:
        request.user.message_set.create(message=_('Impossible discharged of the service. Exist referral to this professional.'))
        return HttpResponseRedirect(('/careprofessional/%s/?clss=error' % object.id))

@permission_required_with_403('careprofessional.careprofessional_write')
def order(request, object_id=None, is_student=False):
    object = get_object_or_404(CareProfessional, pk=object_id, person__organization=request.user.get_profile().org_active)
    if (object.active == True):
        if object.resp_services.filter(active=True):
            messages.error(request, _('Sorry, you can not disable a responsible professional with active service(s)'))
            messages.error(request, _('<br />Active services: <b>%s</b>') % ', '.join([ i.name for i in object.resp_services.filter(active=True)] ))
            
            return HttpResponseRedirect('/careprofessional/%s/' % object.id)
        object.active = False
    else:
        object.active = True

    object.save(force_update=True)
    
    request.user.message_set.create(message=('%s %s %s' % ( \
        (_('Student') if is_student else _('Professional')), \
        (_('activated') if object.active else _('deactivated')), \
        _('successfully'))))
    return HttpResponseRedirect(('/careprofessional/%s/' % object.id) if not is_student else ('/careprofessional/student/%s/' % object.id))
