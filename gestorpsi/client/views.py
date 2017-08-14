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

import string
from datetime import datetime
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from django.utils import simplejson
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse

from django.conf import settings

from gestorpsi.address.models import Country, State, AddressType, City

from gestorpsi.careprofessional.models import LicenceBoard, CareProfessional
from gestorpsi.careprofessional.views import Profession

from gestorpsi.service.models import Service, ServiceGroup, GroupMembers

from gestorpsi.client.models import Client, Relation
from gestorpsi.client.forms import FamilyForm

from gestorpsi.document.models import TypeDocument, Issuer
from gestorpsi.internet.models import EmailType, IMNetwork
from gestorpsi.organization.models import Organization

from gestorpsi.person.views import person_save
from gestorpsi.person.models import Person, MaritalStatus

from gestorpsi.company.models import CompanyClient
from gestorpsi.company.forms import CompanyForm, CompanyClientForm

from gestorpsi.phone.models import PhoneType
from gestorpsi.admission.models import ReferralChoice as AdmissionChoice, AdmissionReferral

from gestorpsi.referral.models import Referral, ReferralChoice, IndicationChoice, Indication, Queue, ReferralExternal, ReferralDischarge
from gestorpsi.referral.forms import ReferralForm, ReferralDischargeForm, QueueForm, ReferralExtForm
from gestorpsi.referral.views import _referral_view, _referral_occurrences
from gestorpsi.util.decorators import permission_required_with_403
from gestorpsi.util.views import get_object_or_None

from gestorpsi.schedule.forms import ScheduleOccurrenceForm, OccurrenceConfirmationForm
from gestorpsi.schedule.views import add_event, occurrence_confirmation_form, _datetime_view
from gestorpsi.schedule.models import ScheduleOccurrence, OccurrenceConfirmation

from gestorpsi.contact.models import Contact

from gestorpsi.util.views import write_pdf
from gestorpsi.util.models import Cnae

from gestorpsi.ehr.views import _access_ehr_check_read
from gestorpsi.place.models import Place

def _access_check(request, object=None):
    """
    client read rights
    this method checks if logged professional have rights to read client data
    @object: client

        Access client data:
        ADM, SECT and Responsible for service (referral.service)

        Logged professional/student have a referral for  
        Client have referral with logged user/professional/student is professional service.
    """
        
    # check if user is professional and not admin or secretary. 
    if request.user.groups.filter(name='administrator') or request.user.groups.filter(name='secretary') or request.user.groups.filter(name='administrator_ro'):
        return True

    # check if professional
    if request.user.groups.filter(name='professional') or request.user.groups.filter(name='student'):
        professional_have_referral_with_client = False
        professional_is_responsible_for_service = False
        # professional. lets check if request.user (professional) have referral with this client
        for r in object.referral_set.all():
            if request.user.profile.person.careprofessional in [p for p in r.professional.all()]:
                professional_have_referral_with_client = True

        # professional. lets check if request.user (professional) is responsible for referral service
        for r in object.referral_set.all():
            if request.user.profile.person.careprofessional in [p for p in r.service.responsibles.all()]:
                professional_is_responsible_for_service = True

        # check if client is referred by professional or if professional is owner of this record
        if professional_have_referral_with_client or professional_is_responsible_for_service or object.revision().user == request.user:
            return True

    return False


def _access_check_referral_write(request, referral=None):
    """
    this method checks professional as users when accessing clients
    @referral: referral object
    """

    # new referral form
    if not referral.id:
        return True

    # check if user is professional and not admin or secretary. if it's true, check if professional has referral with this customer
    if request.user.groups.filter(name='administrator') or request.user.groups.filter(name='secretary'):
        return True

    # check if professional or student
    if request.user.groups.filter(name='professional') or request.user.groups.filter(name='student'):

        professional_have_referral_with_client = False
        professional_is_responsible_for_service = False

        # lets check if request.user (professional) have referral with this client
        if request.user.profile.person.careprofessional in [p for p in referral.professional.all()]:
            professional_have_referral_with_client = True
        
        # lets check if request.user (professional) is responsible for this referral service
        if request.user.profile.person.careprofessional in [p for p in referral.service.responsibles.all()]:
            professional_is_responsible_for_service = True

        if professional_have_referral_with_client or professional_is_responsible_for_service:
            return True

    return False


# list all active clients
@permission_required_with_403('client.client_list')
def index(request, deactive = False):
    # Test if clinic administrator has registered services before access client page.
    list_url_base = '/client/list/' if not deactive else '/client/list/deactive/'

    if not Service.objects.filter(active=True, organization=request.user.get_profile().org_active).count():
        msg = _("There's no Service created yet. Please, create one before access Client, ") + " <a href='/service/add'> clique aqui.</a>"
        return render_to_response('client/client_service_alert.html', {'object': msg }, context_instance=RequestContext(request))
    return render_to_response('client/client_list.html', locals(), context_instance=RequestContext(request))


# client home
@permission_required_with_403('client.client_read')
def home(request, object_id=None):
    object = get_object_or_404(Client, pk=object_id, person__organization=request.user.get_profile().org_active)

    # check access by requested user
    if not _access_check(request, object):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    referrals = Referral.objects.charged().filter(client=object)
    referrals_discharged = ReferralDischarge.objects.filter(client=object)

    c=0
    for x in Referral.objects.filter(client=object):
        c += x.past_occurrences().count()

    if not object.is_active():
        messages.info(request,  _('This client is not enabled.'))

    return render_to_response('client/client_home.html',
                                        {
                                        'object': object,
                                        'referrals': referrals,
                                        'referrals_discharged': referrals_discharged,
                                        'service_subscribers': Service.objects.filter(referral__client = object).distinct().count(),
                                        'care_delivered': c,
                                        },
                                        context_instance=RequestContext(request)
                            )


@permission_required_with_403('client.client_list')
def list(request, page=1, initial=None, filter=None, no_paging=False, deactive=False, retrn=False):
    """
        Tiago de Souza Moraes - 06/05/2014
        retrn : string, JSON or HTML
        search person family return JSON
        search client/initial letter return HTML
    """

    user = request.user
    object_list = Client.objects.from_user(user, 'deactive' if deactive else 'active')

    """
        return json
    """
    if retrn == 'json':

        person = {}
        i = 0

        for c in object_list.filter(person__name__icontains=filter):
            person[i] = {
                'id': c.id, # client id
                'name': c.person.name,
            }
            i = i + 1

        return HttpResponse(simplejson.dumps(person, encoding='iso8859-1'), mimetype='application/json')

    """
        return default
        client index / paginator
    """
    list_url_base = '/client/list/' if not deactive else '/client/list/deactive/'

    url_extra = ''
    initial = ''

    if request.GET.get('initial'):
        initial = request.GET.get('initial')
        
        if ord(initial) < 90:
            initial_next = chr(ord(initial) + 1)

        if ord(initial) > 65:
            initial_prev = chr(ord(initial) - 1)

        object_list = object_list.filter(person__name__istartswith = initial)
        url_extra += '&initial=%s' % initial

    if request.GET.get('search'):
        search = request.GET.get('search')
        object_list = object_list.filter(person__name__icontains = search)
        url_extra += '&search=%s' % search

    # filters
    if request.GET.get('service'):
        service = request.GET.get('service')
        object_list = object_list.filter(referral__service=service).distinct()
        url_extra += '&service=%s' % service
    
    client_service_pk_list = []

    # subscribed
    subscribed = True if request.GET.get('subscribed') == 'true' else False
    if subscribed:
        if not request.GET.get('service'):
            object_list = object_list.filter(referral__service__isnull=False).distinct()
        else:
            for c in object_list:
                for r in c.referrals_charged():
                    if r.service.pk == request.GET.get('service') and c.pk not in client_service_pk_list:
                        client_service_pk_list.append(c.pk)
                        break
        
        url_extra += '&subscribed=%s' % subscribed
    

    # discharged
    discharged = True if request.GET.get('discharged') == "true" else False
    if discharged:
        if not request.GET.get('service'):
            object_list = object_list.filter(referral__referraldischarge__isnull=False).distinct()
        else:
            for c in object_list:
                for r in c.referrals_discharged():
                    if r.service.pk == request.GET.get('service') and c.pk not in client_service_pk_list:
                        client_service_pk_list.append(c.pk)
                        break

        url_extra += '&discharged=%s' % discharged


    # queued
    queued = True if request.GET.get('queued') == "true" else False
    if queued:
        queued = request.GET.get('queued')
        object_list = object_list.filter(referral__queue__isnull=False).distinct()
            
        url_extra += '&queued=%s' % queued


    # nooccurrences
    nooccurrences = True if request.GET.get('nooccurrences') == "true" else False
    if nooccurrences:
        nooccurrences = request.GET.get('nooccurrences')
        object_list = object_list.filter(referral__occurrence__isnull=True).distinct()
        url_extra += '&nooccurrences=%s' % nooccurrences


    # service filter
    if client_service_pk_list: # exclude filtered for charged and discharged results
        object_list = object_list.filter(pk__in=client_service_pk_list)
    

    # paginator result
    p = Paginator(object_list, settings.PAGE_RESULTS)
    page_number = 1 if not request.GET.get('page') else request.GET.get('page')
    page = p.page(page_number)
    object_list = page.object_list
    

    # mount page
    service_list = Service.objects.filter( active=True, organization=request.user.get_profile().org_active )
    initials = string.uppercase

    return render_to_response('tags/list_item.html', locals(), context_instance=RequestContext(request))



@permission_required_with_403('client.client_read')
def form(request, object_id=False, is_company=False):
    """
        client or company render form
        object_id : Client.id
        is_company : Boolean
            render form to company
    """

    # edit
    if object_id :

        object = get_object_or_404(Client, pk=object_id, person__organization=request.user.get_profile().org_active)

        # check access by requested user
        if not _access_check(request, object):
            return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    # new object
    else:
        object = Client()

    # to check registered service
    if not Service.objects.filter(active=True, organization=request.user.get_profile().org_active).count():

        msg = _("There's no Service created yet. Please, create one before access Client, ") + " <a href='/service/add'> clique aqui.</a>"

        return render_to_response('client/client_service_alert.html', {'object': msg }, context_instance=RequestContext(request))

    try:
        cities = City.objects.filter(state=request.user.get_profile().org_active.address.all()[0].city.state)
    except:
        cities = {}

    # default is person
    template_name = 'client/client_form.html'

    # company
    cnae = None
    company_form = None

    if is_company:
        template_name = 'client/client_form_company.html'

        if object_id:
            company_form = CompanyForm(instance=object.person.company)
            cnae = get_object_or_None(Cnae, pk=object.person.company.cnae_class)
        else:
            company_form = CompanyForm()
            cnae = Cnae.objects.all()

    # edit
    if object_id:
        return render_to_response(template_name,
                                  {
                                    'object': object,
                                    'company_form': company_form,
                                    'phones' : object.person.phones.all(),
                                    'addresses' : object.person.address.all(),
                                    'documents' : object.person.document.all(),
                                    'emails' : object.person.emails.all(),
                                    'websites' : object.person.sites.all(),
                                    'ims' : object.person.instantMessengers.all(),
                                    'notify' : None if not object.person.notify.filter(org_id=request.user.profile.org_active.id) else object.person.notify.get(org_id=request.user.profile.org_active.id),
                                    'PhoneTypes': PhoneType.objects.all(), 
                                    'AddressTypes': AddressType.objects.all(), 
                                    'EmailTypes': EmailType.objects.all(), 
                                    'IMNetworks': IMNetwork.objects.all(), 
                                    'TypeDocuments': TypeDocument.objects.filter(source=1), 
                                    'Issuers': Issuer.objects.all(), 
                                    'countries': Country.objects.all(),
                                    'States': State.objects.all(), 
                                    'Cities': cities,
                                    'MaritalStatusTypes': MaritalStatus.objects.all(), 
                                    'PROFESSIONAL_AREAS': Profession.objects.all(),
                                    'licenceBoardTypes': LicenceBoard.objects.all(),
                                    'ReferralChoices': ReferralChoice.objects.all(),
                                    'Relations': Relation.objects.all(),
                                    'cnae': cnae,
                                   },
                                    context_instance=RequestContext(request)
                            )
    # new
    else:
        return render_to_response(template_name,
                                   {
                                    'company_form': company_form,
                                    'PhoneTypes': PhoneType.objects.all(), 
                                    'AddressTypes': AddressType.objects.all(), 
                                    'EmailTypes': EmailType.objects.all(), 
                                    'IMNetworks': IMNetwork.objects.all() , 
                                    'TypeDocuments': TypeDocument.objects.filter(source=1), 
                                    'Issuers': Issuer.objects.all(), 
                                    'countries': Country.objects.all(),
                                    'States': State.objects.all(), 
                                    'Cities': cities,
                                    'MaritalStatusTypes': MaritalStatus.objects.all(),
                                    'PROFESSIONAL_AREAS': Profession.objects.all(),
                                    'licenceBoardTypes': LicenceBoard.objects.all(),
                                    'ReferralChoices': ReferralChoice.objects.all(),
                                    'Relations': Relation.objects.all(),
                                    'cnae': cnae,
                                   },
                                    context_instance=RequestContext(request)
                            )


@permission_required_with_403('referral.referral_read')
def referral_int_form(request, object_id=None, referral_id=None):
    """
        Internal referral, referral of referral.
        This function render a form and save.

        object_id : Client.id
        referral_id : Referral.id
    """

    object = get_object_or_404( Client, pk=object_id, person__organization=request.user.get_profile().org_active )
    referral = get_object_or_404( Referral, pk=referral_id, service__organization=request.user.get_profile().org_active )

    # check access by requested user
    if not _access_check(request, object) or not _access_check_referral_write(request, referral):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    if request.method == 'POST':

        form = ReferralForm(request, request.POST)

        if form.is_valid():

            data = form.save(commit=False)
            data.organization = request.user.get_profile().org_active
            data.referral = referral # referral of referral
            data.status = '01'
            # commit
            data.save()
            # add client
            data.client.add(object)
            # save professionals
            form.save_m2m()

            ''' if asked, add referral and client to some existing group ''' 
            GroupMembers.objects.filter( client=object, client__person__organization=request.user.get_profile().org_active, referral=data).delete()
            if data.service.is_group and request.POST.get('group'):
                group = get_object_or_404(ServiceGroup, pk=request.POST.get('group'), service__organization=request.user.get_profile().org_active)
                gm = GroupMembers(group=group, client=object, referral=data)
                gm.save()

        messages.success(request, _('Referral saved successfully'))
        return HttpResponseRedirect(reverse('client-referral-home', args=[object.id,data.id]) )

    else:
        form = ReferralForm(request)

    # render form
    return render_to_response('client/client_referral_int_form.html',
                              { 'object': object, 
                                'referral': referral,
                                'referral_form': form,
                               }, context_instance=RequestContext(request))


@permission_required_with_403('referral.referral_read')
def referral_form(request, object_id=None, referral_id=None):
    '''
        new, alter and save Referral
        object_id : Client.id
        referral_id : Referral.id
    '''
    # client
    object = get_object_or_404( Client, pk=object_id, person__organization=request.user.get_profile().org_active )

    # check access by requested user
    if not _access_check(request, object):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))
    
    if not object.active:
        return render_to_response('403.html', {'object': _("Sorry! You can not save referral for disabled clients!"), }, context_instance=RequestContext(request))

    if referral_id:
        referral = get_object_or_404(Referral, pk=referral_id, service__organization=request.user.get_profile().org_active)
    else:
        referral = Referral()

    # to check permission
    if not _access_check_referral_write(request, referral):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))
    
    # post
    if request.method == 'POST':

        referral_form = ReferralForm( request, request.POST, instance=referral )

        if referral_form.is_valid():

            data = referral_form.save(commit=False)
            data.organization = request.user.get_profile().org_active
            data.status = '01'

            if data.service.active:

                data.save()
                # add client
                data.client.add(object)
                # save m2m relation
                referral_form.save_m2m()

                ''' Indication  Section '''
                if request.POST.get('indication'):
                    referral.indication_set.all().delete()
                    indication = Indication()
                    indication.indication_choice = IndicationChoice.objects.get(pk=request.POST.get('indication'))
                    indication.referral_organization = get_object_or_None(Organization, id=request.POST.get('indication_organization'))
                    indication.referral_professional = get_object_or_None(CareProfessional, id=request.POST.get('indication_professional'))
                    indication.referral = Referral.objects.get(pk = data)
                    indication.save()

                ''' if asked, add referral and client to some existing group ''' 
                GroupMembers.objects.filter( client=object, client__person__organization=request.user.get_profile().org_active, referral=data).delete()

                if data.service.is_group and request.POST.get('group'):
                    group = get_object_or_404(ServiceGroup, pk=request.POST.get('group'), service__organization=request.user.get_profile().org_active)
                    gm = GroupMembers(group=group, client=object, referral=data)
                    gm.save()
                
                url = '/client/%s/referral/%s/'
                msg = _('Referral saved successfully')
                messages.success(request, _(msg))
                return HttpResponseRedirect(url % (object_id, data.id))

    # not post, render form for new or update register.
    else:
        if referral.id:
            referral_form = ReferralForm(request, instance=referral)
        else:
            referral_form = ReferralForm(request)

    return render_to_response('client/client_referral_form.html',
                                  { 'object': object, 
                                    'referral': referral,
                                    'referral_form': referral_form,
                                    'referral_list': Referral.objects.filter(client=object, status='01'),
                                    'access_check_referral_write': _access_check_referral_write(request, referral),
                                    'IndicationsChoices': IndicationChoice.objects.all(),
                                    'contact_organizations': Contact.objects.filter_internal(
                                                    org_id = request.user.get_profile().org_active.id, 
                                                    person_id = request.user.get_profile().person.id, 
                                                    filter_name = None,
                                                    filter_type = 1
                                                ),
                                    'contact_professionals': Contact.objects.filter_internal(
                                                    org_id = request.user.get_profile().org_active.id, 
                                                    person_id = request.user.get_profile().person.id, 
                                                    filter_name = None,
                                                    filter_type = 2
                                                ),
                                    'contact_organizations_external': Contact.objects.filter_external(
                                                    org_id = request.user.get_profile().org_active.id, 
                                                    person_id = request.user.get_profile().person.id, 
                                                    filter_name = None,
                                                    filter_type = 1
                                                ),
                                    'contact_professionals_external': Contact.objects.filter_external(
                                                    org_id = request.user.get_profile().org_active.id, 
                                                    person_id = request.user.get_profile().person.id, 
                                                    filter_name = None,
                                                    filter_type = 2
                                                ),
                                   },
                                   context_instance=RequestContext(request)
                              )


@permission_required_with_403('referral.referral_read')
def referral_discharge_form(request, object_id = None, referral_id = None, discharge_id = None):
    object = get_object_or_404(Client, pk = object_id, person__organization=request.user.get_profile().org_active)
    referral = get_object_or_404(Referral, pk=referral_id, service__organization=request.user.get_profile().org_active)

    # check access by requested user
    if not _access_check(request, object) or not _access_check_referral_write(request, referral):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    if referral.on_queue():
        messages.error(request, _('Sorry, you can not discharge a queued referral. Remove it from queue first before to continue'))
        return HttpResponseRedirect('/client/%s/referral/%s/' % (object.id, referral.id))

    instance = None

    if discharge_id:
        if not referral.referraldischarge_set.filter(pk=discharge_id):
            raise Http404
        else:
            instance = referral.referraldischarge_set.get(pk=discharge_id)

    if referral.upcoming_occurrences().count() == 0 or instance:
        if request.method == 'POST':
            if not instance:
                form = ReferralDischargeForm(request.POST, initial=dict(client=object, referral=referral))
            else:
                form = ReferralDischargeForm(request.POST, instance=instance, initial=dict(client=object, referral=referral))

            if form.is_valid():
                data = form.save(commit=False)
                data.client = object
                data.referral = referral
                data.save()
                if not instance:
                    messages.success(request, _('Client discharged successfully'))
                else:
                    messages.success(request, _('Referral discharge updated successfully'))
                return HttpResponseRedirect('/client/%s/home/' % (object.id))
            else:
                messages.error(request, _('Form Error'))
                return render_to_response('client/client_referral_discharge_form.html', locals(), context_instance=RequestContext(request))
        else:
            if not instance:
                form = ReferralDischargeForm(initial=dict(client=object, referral=referral))
            else:
                form = ReferralDischargeForm(instance=instance, initial=dict(client=object, referral=referral))

        return render_to_response('client/client_referral_discharge_form.html', locals(), context_instance=RequestContext(request))

    else:
        messages.info(request, _('Registered have hour in the schedule'))
        return HttpResponseRedirect('/client/%s/referral/%s/' % (object.id, referral.id))


@permission_required_with_403('referral.referral_list')
def referral_list(request, object_id=None, discharged=None):
    object = get_object_or_404(Client, pk = object_id, person__organization=request.user.get_profile().org_active)

    # check access by requested user
    if not _access_check(request, object):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    if discharged:
        referrals = object.referrals_discharged()
    else:
        referrals = object.referrals_charged()
        charged = True
    
    return render_to_response('client/client_referral_list.html', locals(), context_instance=RequestContext(request))


@permission_required_with_403('referral.referral_read')
def referral_home(request, object_id=None, referral_id=None):
    object = get_object_or_404(Client, pk=object_id, person__organization=request.user.get_profile().org_active)

    # check access by requested user
    if not _access_check(request, object):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    access_check_referral_write = False
    if _access_check_referral_write(request, get_object_or_404(Referral, pk=referral_id, service__organization=request.user.get_profile().org_active)):
        access_check_referral_write = True

    return _referral_view(request, object_id, referral_id, 'client/client_referral_home.html', access_check_referral_write)


@permission_required_with_403('client.client_write')
def save(request, object_id=None, is_company=False):
    """
       Save or Update a client record
    """
    user = request.user

    if not request.POST:
        return HttpResponseRedirect('/client/add/')

    if object_id:
        object = get_object_or_404(Client, pk=object_id, person__organization=request.user.get_profile().org_active)
        person = object.person

        # check access by requested user
        if not _access_check(request, object):
            return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    else:
        object = Client()
        person = Person()
        
        # Id Record
        org = get_object_or_404(Organization, pk=user.get_profile().org_active.id )
        org.last_id_record = org.last_id_record + 1
        org.save()

        # Admission date
        object.idRecord = org.last_id_record + 1
        object.admission_date = datetime.now()

    # person
    object.person = person_save(request, person)
    
    if is_company:
        company_form = CompanyForm(request.POST) if not object_id else CompanyForm(request.POST, instance=object.person.company)

        if company_form.is_valid():
            company = company_form.save(commit=False)
            company.person = object.person
            company.save()

    # automatic admit client
    a = AdmissionReferral()
    if object.admissionreferral_set.all():
        a = object.admissionreferral_set.all()[0]

    # save update
    object.save()

    a.referral_choice_id = AdmissionChoice.objects.all().order_by('weight')[0].id
    object.admissionreferral_set.add(a)

    # save update
    object.save()
    
    messages.success(request, _('Client saved successfully'))
    return HttpResponseRedirect('/client/%s/home' % object.id)


@permission_required_with_403('client.client_read')
def client_print(request, object_id = None):

    object = get_object_or_404( Client, pk=object_id, person__organization=request.user.get_profile().org_active )

    # check access by requested user
    if not _access_check(request, object):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    have_ehr_read_perms = False if not _access_ehr_check_read(request, object) else True
    
    if request.POST:

        referral = object.referral_set.filter(pk__in=request.POST.getlist('referral'))
        print_schedule = None if not request.POST.get('schedule') else True
        print_demographic = None if not request.POST.get('demographic') else True
        print_ehr = None if not request.POST.get('ehr') else True
        signed_professional_responsible = None if not request.POST.get('signed_professional_responsible') else True
        signed_professionals = None if not request.POST.get('signed_professionals') else True
        signed_organization_reponsibles = None if not request.POST.get('signed_organization_reponsibles') else True

        company_related_clients = []
        if object.is_company():
            company_related_clients = CompanyClient.objects.filter(company__person__client = object, company__person__organization=request.user.get_profile().org_active)

        dict = {
            'referral': referral,
            'print_schedule': print_schedule,
            'print_demographic': print_demographic,
            'signed_professional_responsible': signed_professional_responsible,
            'signed_professionals': signed_professionals,
            'signed_organization_reponsibles': signed_organization_reponsibles,
            'print_ehr': print_ehr,
            'pagesize' : 'A4',
            'object': object, 
            'org_active': request.user.get_profile().org_active, 
            'user': request.user, 
            'DEBUG': DEBUG, 
            'settings.MEDIA_URL': settings.MEDIA_URL if request.POST.get('output') == 'html' else settings.MEDIA_ROOT.replace('\\','/') + '/', 
            'company_related_clients': company_related_clients,
            'have_ehr_read_perms': have_ehr_read_perms,
            'all_payments': request.POST.get('all_payments'),
            }

        # output format
        if request.POST.get('output') == 'html':
            return render_to_response('client/client_print.html', dict, context_instance=RequestContext(request))

        if request.POST.get('output') == 'pdf':
            return write_pdf('client/client_print.html', dict, '%s.pdf' % slugify(object.person.name))

    else:

        return render_to_response('client/client_print_form.html', locals(), context_instance=RequestContext(request))


@permission_required_with_403('client.client_read')
def organization_clients(request):
    """
       organization_clients: return json with all clients from logged organization
    """

    if not request.GET.get('include_deactivated'):
        clients = Client.objects.from_user(request.user, 'active').order_by('person__name')
    else:
        clients = Client.objects.from_user(request.user).order_by('person__name')
    
    if request.GET.get('q'):
        clients = clients.filter(person__name__istartswith=request.GET.get('q'))
    
    dict = {}
    array = []

    for o in clients:
        c = {
            'id': o.id,
            'name': u'%s%s%s' % (o.person.name, '' if not o.person.is_company() else _(' (Company)'), '' if o.active == True else _(' (Disabled)')),
        }
        array.append(c)

    dict['results'] = array
    array = simplejson.dumps(dict, encoding = 'iso8859-1')

    #return HttpResponse(array, mimetype='application/json')
    return HttpResponse(array)

@permission_required_with_403('client.client_write')
def order(request, object_id = ''):
    object = get_object_or_404(Client, pk = object_id, person__organization=request.user.get_profile().org_active)

    # check access by requested user
    if not _access_check(request, object):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    url = '/client/%s/home/'

    if not object.is_active():
        messages.success(request, _('User activated successfully'))
        object.set_active()
    else:
        if Referral.objects.charged().filter(client = object).count() == 0:
            object.set_deactive()
            messages.success(request, _('User deactivated successfully'))
        else:
            messages.error(request, _('Sorry, you can not deactivate a client with registered referral'))
        
    return HttpResponseRedirect(url % object.id)

@permission_required_with_403('schedule.schedule_read')
def schedule_daily(
            request,  
            year = datetime.now().strftime("%Y"),
            month = datetime.now().strftime("%m"), 
            day = datetime.now().strftime("%d"), 
            template='client/client_schedule_daily.html',
            **params
        ):

    # verify if user has perm
    referral = get_object_or_404(Referral, pk=request.GET.get('referral'), service__organization=request.user.get_profile().org_active)

    if not _access_check(request, get_object_or_404(Client, pk=request.GET.get('client'), person__organization=request.user.get_profile().org_active)):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    if referral.on_queue():
        messages.error(request, _('Sorry, you can not book a queued client. Remove it first from queue before continue'))
        return HttpResponseRedirect('/client/%s/referral/%s/' % (request.GET.get('client'), referral.id))
    
    if Place.objects.filter( organization=request.user.get_profile().org_active, place_type__id=1 ):
        place = Place.objects.filter( organization=request.user.get_profile().org_active, place_type__id=1 )[0] # place type = matriz
    else:
        place = Place.objects.filter( organization=request.user.get_profile().org_active, )[0] # first

    return _datetime_view(request, template, datetime(int(year), int(month), int(day)), place.id, referral = request.GET['referral'], client = request.GET['client'], **params)

@permission_required_with_403('schedule.schedule_write')
def schedule_add(request):

    # verify if user has perm
    referral = get_object_or_404(Referral, pk=request.GET.get('referral'), service__organization=request.user.get_profile().org_active)

    if not _access_check_referral_write(request, referral):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    return add_event(request, 
        'client/client_schedule_form.html', 
        event_form_class=ReferralForm(request),
        recurrence_form_class=ScheduleOccurrenceForm,
        redirect_to = '/client/%s/referral/%s/' % (request.GET['client'], request.GET['referral']))

@permission_required_with_403('schedule.schedule_read')
def occurrence_view(request, object_id = None, occurrence_id = None):
    occurrence = get_object_or_404(ScheduleOccurrence, pk = occurrence_id, event__referral__service__organization=request.user.get_profile().org_active)

    return occurrence_confirmation_form(request,
        occurrence_id,
        template = 'client/client_occurrence_confirmation_form.html', 
        form_class=OccurrenceConfirmationForm,
        client_id=object_id,
        redirect_to = '/client/%s/referral/%s/' % (object_id, occurrence.event.referral.id)
        )


@permission_required_with_403('schedule.schedule_list')
def referral_occurrences(request, object_id=None, referral_id=None, type='upcoming'):

    if not _access_check(request, get_object_or_404(Client, pk=object_id, person__organization=request.user.get_profile().org_active)):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    return _referral_occurrences(request, object_id, referral_id, type, 'client/client_referral_occurrences.html')


@permission_required_with_403('schedule.schedule_list')
def referral_occurrences_action(request, object_id=None, referral_id=None):
    '''
        confirmation of one or lot of occurrences
    '''

    msg = False
    c = 0

    for x in request.POST.getlist('list_occurrence'):

        # get object and check org to avoid hack.
        oc = get_object_or_404( ScheduleOccurrence, pk=x, event__referral__organization=request.user.get_profile().org_active )

        ocf = OccurrenceConfirmation()
        ocf.occurrence = oc
        ocf.presence = request.POST.get('id_action')
        ocf.reason = request.POST.get('reason')
        ocf.save()

        c += 1
        msg = True

    if msg:
        messages.success(request, _(u'Ocorrência salvo com sucesso! Total de %s' % c ))

    # return to list of futures events
    return HttpResponseRedirect('/client/%s/referral/%s/upcoming/' % (object_id, referral_id) )

    
@permission_required_with_403('referral.referral_read')
def referral_queue(request, object_id = '',  referral_id = ''):
    object = get_object_or_404(Client, pk = object_id, person__organization=request.user.get_profile().org_active)

    # check access by requested user
    if not _access_check(request, object):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    referral = get_object_or_404(Referral, pk=referral_id, service__organization=request.user.get_profile().org_active)

    if not _access_check_referral_write(request, referral):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    if referral.on_queue():
        messages.error(request, _('Error adding to queue! Referral is already queued'))
        return HttpResponseRedirect('/client/%s/referral/%s/' % (object.id, referral.id))

    if referral.upcoming_occurrences():
        messages.error(request, _('Error adding to queue! Referral have upcoming occurrences'))
        return HttpResponseRedirect('/client/%s/referral/%s/' % (object.id, referral.id))

    form=QueueForm()
    return render_to_response("client/client_referral_queue.html", locals(), context_instance=RequestContext(request))

@permission_required_with_403('referral.referral_write')
def referral_queue_save(request, object_id = '',  referral_id = ''):
    object = get_object_or_404(Client, pk = object_id, person__organization=request.user.get_profile().org_active)

    # check access by requested user
    if not _access_check(request, object):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    referral = get_object_or_404(Referral, pk=referral_id, service__organization=request.user.get_profile().org_active)

    if referral.on_queue():
        messages.error(request, _('Error adding to queue! Referral is already queued'))
        return HttpResponseRedirect('/client/%s/referral/%s/' % (object.id, referral.id))

    if referral.upcoming_occurrences():
        messages.error(request, _('Subscript in the queue not is possible. Referral have upcoming occurrences'))
        return HttpResponseRedirect('/client/%s/referral/%s/' % (object.id, referral.id))

    form = QueueForm(request.POST)

    if form.is_valid():
        object_q = Queue()
        object_q = form.save(commit=False)
        try:
            if referral.priority.title == 'Alta':
                object_q.priority = '01'
            elif referral.priority.title == u'Média':
                object_q.priority = '02'
            else:
                object_q.priority = '03'
        except:
            object_q.priority = '03'
        object_q.save()

    messages.success(request, _('Referral added to queue successfully'))
    return HttpResponseRedirect('/client/%s/referral/%s/' % (object.id, referral.id))

@permission_required_with_403('referral.referral_write')
def referral_queue_remove(request, object_id = '',  referral_id = '', queue_id = ''):

    """ This action don't remove the register, just save date out of the register """
    object = get_object_or_404(Client, pk = object_id, person__organization=request.user.get_profile().org_active)

    # check access by requested user
    if not _access_check(request, object):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    referral = get_object_or_404(Referral, pk=referral_id, service__organization=request.user.get_profile().org_active)
    queue = get_object_or_None(Queue, pk = queue_id)
    
    queue.date_out = datetime.now()
    queue.save()

    messages.success(request, _('Client removed from queue successfully'))
    return HttpResponseRedirect('/client/%s/referral/%s/' % (object.id, referral.id))

@permission_required_with_403('referral.referral_read')
def referral_ext_form(request, object_id ='', referral_id=''):
    object = get_object_or_404(Client, pk = object_id, person__organization=request.user.get_profile().org_active)
    referral = get_object_or_404(Referral, pk=referral_id, service__organization=request.user.get_profile().org_active)

    # check access by requested user
    if not _access_check(request, object) or not _access_check_referral_write(request, referral):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    contact_organizations = Contact.objects.filter(
                                                org_id = request.user.get_profile().org_active.id, 
                                                person_id = request.user.get_profile().person.id, 
                                                filter_name = None,
                                                filter_type = 1
                                                )

    form = ReferralExtForm()
    return render_to_response('client/client_referral_ext_form.html', locals(), context_instance=RequestContext(request))

@permission_required_with_403('referral.referral_write')
def referral_ext_save(request, object_id = '', referral_id=''):
    object = get_object_or_404(Client, pk = object_id, person__organization=request.user.get_profile().org_active)

    # check access by requested user
    if not _access_check(request, object):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    referral = get_object_or_404(Referral, pk=referral_id, service__organization=request.user.get_profile().org_active)
    form = ReferralExtForm(request.POST) 
    queues = Queue.objects.filter(referral=referral_id)
    referrals = ReferralExternal.objects.filter(referral=referral_id)

    if form.is_valid():
        referral_ext = ReferralExternal() 
        referral_ext = form.save(commit=False)
        referral_ext.professional = get_object_or_None(CareProfessional, pk = request.POST.get('professional') )
        referral_ext.organization = get_object_or_None(Organization, pk = request.POST.get('organization') )
        referral_ext.save()

    messages.success(request, _('External Referral saved successfully'))
    return render_to_response('client/client_referral_home.html', locals(), context_instance=RequestContext(request))

@permission_required_with_403('client.client_read')
def family(request, object_id = None):
    object = get_object_or_404(Client, pk = object_id, person__organization=request.user.get_profile().org_active)

    # check access by requested user
    if not _access_check(request, object):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    return render_to_response('client/client_family.html', locals(), context_instance=RequestContext(request))

@permission_required_with_403('client.client_write')
def family_form(request, object_id = None, relation_id=None):
    object = get_object_or_404(Client, pk = object_id, person__organization=request.user.get_profile().org_active)

    # check access by requested user
    if not _access_check(request, object):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    if relation_id:
        from gestorpsi.client.models import Family
        relation = get_object_or_404(Family, \
            pk=relation_id, \
            client__person__organization=request.user.get_profile().org_active, \
            client_related__person__organization=request.user.get_profile().org_active, \
        )

    if request.method == 'POST':
        form = FamilyForm(request.POST, instance=relation) if relation_id else FamilyForm(request.POST)
        if form.is_valid():
            if not relation_id:
                data = form.save(request, object)
            else:
                relation.responsible = True if request.POST.get('responsible') else False
                relation.relation_level = None if not request.POST.get('relation_level') else request.POST.get('relation_level')
                relation.active = True if request.POST.get('active') else False
                relation.comment = request.POST.get('comment') or ''
                relation.save()
            messages.success(request, _('Family member added successfully'))
            return HttpResponseRedirect('/client/%s/family/' % object.id)
        else:
            return render_to_response('client/client_family_form.html', locals(), context_instance=RequestContext(request))

    else:
        if relation_id:
            from django import forms
            form = FamilyForm(instance=Family.objects.get(pk=relation.id))
            form.fields['name'].widget = forms.TextInput(attrs={'readonly':'readonly', 'class':'extrabig'})
            if not relation.client == object:
                is_reverse = True
                from gestorpsi.client.models import FAMILY_RELATION_REVERSE
                form.fields['relation_level'].choices = FAMILY_RELATION_REVERSE
                name = relation.client
            else:
                is_reverse = False
                name = relation.client_related

            form.fields['name'].initial = name
        else:
            form = FamilyForm()

    return render_to_response('client/client_family_form.html', locals(), context_instance=RequestContext(request))

@permission_required_with_403('client.client_list')
def company_related(request, object_id = None):
    object = get_object_or_404(Client, pk = object_id, person__organization=request.user.get_profile().org_active)

    # check access by requested user
    if not _access_check(request, object):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    clients = CompanyClient.objects.filter(company__person__client = object, company__person__organization=request.user.get_profile().org_active)

    return render_to_response('client/client_company_related.html', locals(), context_instance=RequestContext(request))

@permission_required_with_403('client.client_write')
def company_related_form(request, object_id = None, company_client_id=None):
    object = get_object_or_404(Client, pk = object_id, person__organization=request.user.get_profile().org_active)

    # check access by requested user
    if not _access_check(request, object):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    form = CompanyClientForm()
    if company_client_id:
        company_client = get_object_or_404(CompanyClient, \
            pk=company_client_id, \
            company__person__organization=request.user.get_profile().org_active, \
            client__person__organization=request.user.get_profile().org_active, \
            )
        form = CompanyClientForm(instance=company_client)
        
        from django import forms
        form.fields['name'].widget = forms.TextInput(attrs={'readonly':'readonly', 'class':'extrabig'})
        form.fields['name'].initial = company_client.client

    if request.method == 'POST':
        if request.POST.get('client_id') in [i.client.pk for i in object.employees()]:
            messages.info(request, _('Employee already registered on this company'))
            return HttpResponseRedirect('/client/%s/company_clients/' % object.id)

        if company_client_id:
            form = CompanyClientForm(request.POST, instance=company_client)
        else:
            form = CompanyClientForm(request.POST)
            
        if form.is_valid():
            form.save(request, object)
            messages.success(request, _('Related client added successfully to this company'))
            return HttpResponseRedirect('/client/%s/company_clients/' % object.id)
        else:
            return render_to_response('client/client_company_related_form.html', locals(), context_instance=RequestContext(request))

    return render_to_response('client/client_company_related_form.html', locals(), context_instance=RequestContext(request))
