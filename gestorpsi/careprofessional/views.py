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
from django.contrib import messages
from gestorpsi.person.models import Person, MaritalStatus
from gestorpsi.person.views import person_json_list, person_save
from gestorpsi.careprofessional.models import ProfessionalProfile, ProfessionalIdentification, CareProfessional, Profession
from gestorpsi.careprofessional.forms import StudentProfileForm
from gestorpsi.phone.models import PhoneType
from gestorpsi.address.models import Country, State, AddressType, City
from gestorpsi.internet.models import EmailType, IMNetwork
from gestorpsi.document.models import TypeDocument, Issuer
from gestorpsi.place.models import Place, PlaceType, HOURS
from gestorpsi.service.models import Service
from gestorpsi.referral.models import Referral, ReferralDischargeReason, ReferralDischarge
from gestorpsi.util.decorators import permission_required_with_403
from gestorpsi.util.views import get_object_or_None
from gestorpsi.schedule.models import OccurrenceConfirmation
from gestorpsi.client.models import Client


@permission_required_with_403('careprofessional.careprofessional_list')
def index(request, template_name='careprofessional/careprofessional_list.html', deactive=False):

    # show active tab
    if deactive:
        action_tab_deactive = True
    else:
        action_tab_index = True

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

  
@permission_required_with_403('careprofessional.careprofessional_list')
def list(request, page=1, deactive=False, filter=None, initial=None, no_paging=False, is_student=False ):

    # professional
    if not is_student:
        if deactive:
            object = CareProfessional.objects.deactive(request.user.get_profile().org_active)
        else:
            object = CareProfessional.objects.active(request.user.get_profile().org_active)
    # stundent
    else:
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
def form(request, object_id=None, template_name='careprofessional/careprofessional_form.html', is_student=False):

    if object_id:
        object = get_object_or_404(CareProfessional, pk=object_id, person__organization=request.user.get_profile().org_active)
        tab = 'edit'
    else:
        if not request.user.has_perm('careprofessional.careprofessional_write'):
            return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

        tab = 'add'
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

    if not object.active:
        messages.info(request,  _('This professional is not enabled.'))

    return render_to_response(template_name, {
                                    'object': object,
                                    'student_form': student_form if is_student else None,
                                    'phones' : None if not hasattr(object, 'person') else object.person.phones.all(),
                                    'addresses' : None if not hasattr(object, 'person') else object.person.address.all(),
                                    'documents' : None if not hasattr(object, 'person') else object.person.document.all(),
                                    'emails' : None if not hasattr(object, 'person') else object.person.emails.all(),
                                    'websites' : None if not hasattr(object, 'person') else object.person.sites.all(),
                                    'ims' : None if not hasattr(object, 'person') else object.person.instantMessengers.all(),
                                    'PROFESSIONAL_AREAS': Profession.objects.all(),
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
                                    'ReferralDischargeReason': None if not object.have_referral_charged else ReferralDischargeReason.objects.all(),
                                    'hours': HOURS,
                                    'action_tab_form': tab, # show tab active
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

    '''
        remove service before add
        check if service have referral before remove.
        cannot be removed if have referral.
    '''
    # all service that are in list_service cannot be removed because it have referral. Create a error message for service and show to user.
    list_to_remove = []

    # remove service, compare from form and db.
    for x in object.prof_services.all(): # professional
        if not x.id in request.POST.getlist('professional_service'):
            # check referral
            if Referral.objects.charged().filter( professional=object, service=x, status='01'):
                list_to_remove.append(x) # add to msg
            else:
                object.prof_services.remove(x) # remove from professional

    # add new service to professional
    for x in request.POST.getlist('professional_service'):
        object.prof_services.add(x) # no problem to replace


    profile = get_object_or_None(ProfessionalProfile, pk=object.professionalProfile_id) or ProfessionalProfile()
    profile.initialProfessionalActivities = request.POST.get('professional_initialActivitiesDate')
    profile.save()
    object.professionalProfile = profile

    # remove all workplace
    profile.workplace.clear()
    # update workplace
    for x in request.POST.getlist('professional_workplace'):
        profile.workplace.add( Place.objects.get( pk=x, organization=request.user.get_profile().org_active ) )

    if not is_student:

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
    return object, list_to_remove


@permission_required_with_403('careprofessional.careprofessional_write')
def save(request, object_id=None, save_person=True, is_student=False):

    if is_student: # verify if student can join in service
        for ps in request.POST.getlist('professional_service'):
            if not Service.objects.filter(active=True, organization=request.user.get_profile().org_active, academic_related=True, pk=ps):
                return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    object, list_to_remove = save_careprof(request, object_id, save_person, is_student)

    if is_student:
        student_form = StudentProfileForm(request.POST, instance=object.studentprofile) if object_id else StudentProfileForm(request.POST)
        if student_form.is_valid():
            data = student_form.save(commit=False)
            data.professional = object
            data.save()

    # one of service have referral and can't be removed from professional.
    if list_to_remove:

        # msg error
        for x in list_to_remove:
            try:
                msg += u', %s' % x.name
            except:
                msg = u'%s' % x.name

        # english error message
        #messages.error(request, _('Impossible discharged of the service. Exist referral to this professional. Service(s) <br /> %s' % msg ))
        #return HttpResponseRedirect(('/careprofessional/%s/' % object.id))

        messages.error(request, _(u'Serviço não pode ser desligado. Existe inscrição para esse profissional. Serviço<br />%s' % msg ))
        return HttpResponseRedirect(('/careprofessional/%s/' % object.id))
    else:
        messages.success(request, _('Professional saved successfully') if not is_student else _('Student saved successfully'))
        return HttpResponseRedirect(('/careprofessional/%s/' % object.id) if not is_student else ('/careprofessional/student/%s/' % object.id))


@permission_required_with_403('careprofessional.careprofessional_write')
def order(request, object_id=None, is_student=False):

    object = get_object_or_404(CareProfessional, pk=object_id, person__organization=request.user.get_profile().org_active)

    if (object.active == True):
        if object.resp_services.filter(active=True):
            messages.error(request, _('Sorry, you can not disable a responsible professional with active service(s)'))
            messages.error(request, _('<br />Active services: <b>%s</b>') % ', '.join([ i.name for i in object.resp_services.filter(active=True)] ))
            
            return HttpResponseRedirect('/careprofessional/%s/' % object.id)
        
        if not object.have_referral_charged():
            object.active = False
        else:
            if request.method == 'POST':
                ## set all upcoming occurrence as unmarked
                for i in object.upcoming_occurrences():
                    o = OccurrenceConfirmation()
                    o.occurrence_id = i.id
                    o.presence = 4 # unmarked
                    o.save()

                # discharge all active 
                reason = get_object_or_404(ReferralDischargeReason, pk=request.POST.get('reason'))
                for r in object.referrals_charged():
                    if r.professional.all().count() > 1:
                        # there is another professional on same referral
                        # just remove it
                        r.professional.remove(object)
                    else:
                        # deative referral
                        for c in r.client.all():
                            rd = ReferralDischarge()
                            rd.referral_id = r.pk
                            rd.client_id = c.pk
                            rd.reason_id = reason.pk
                            rd.details = request.POST.get('details')
                            rd.save()
                object.active = False
    else:
        object.active = True

    object.save(force_update=True)
    
    messages.success(request, ('%s %s %s' % ( \
        (_('Student') if is_student else _('Professional')), \
        (_('activated') if object.active else _('deactivated')), \
        _('successfully'))))
    return HttpResponseRedirect(('/careprofessional/%s/' % object.id) if not is_student else ('/careprofessional/student/%s/' % object.id))


# permission
def client_list(request, object_id=False, active=True):
    """
        list of clients of careprofessional
        id : Careprofessional.id
        active : Client active or inactive
    """
    action_tab_client_list = True # show active tab
    client_list_filter = _('Active') if active == str(1) else _('Inactive') # show filter

    # fix filter
    object = get_object_or_404(CareProfessional, pk=object_id, person__organization=request.user.get_profile().org_active)

    """
        referral have professional and client.
        get all clients of professional by referral.
    """
    # filter by Client.active
    if active == str(1):
        client_list = Client.objects.filter(referral__professional=object, person__organization=request.user.get_profile().org_active, active=True).order_by('person__name').distinct()
    else:
        client_list = Client.objects.filter(referral__professional=object, person__organization=request.user.get_profile().org_active, active=False).order_by('person__name').distinct()

    return render_to_response('careprofessional/careprofessional_client_list.html', locals(), context_instance=RequestContext(request))
