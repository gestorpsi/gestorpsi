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
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from django.utils import simplejson

from geraldo.generators import PDFGenerator

from gestorpsi.address.models import Country, State, AddressType, City
from gestorpsi.authentication.models import Profile
from gestorpsi.careprofessional.models import LicenceBoard, CareProfessional
from gestorpsi.service.models import Service
from gestorpsi.careprofessional.models import CareProfessional
from gestorpsi.careprofessional.views import Profession
from gestorpsi.client.models import Client, Relation
from gestorpsi.client.reports import ClientRecord, ClientList
from gestorpsi.client.forms import FamilyForm
from gestorpsi.document.models import TypeDocument, Issuer
from gestorpsi.internet.models import EmailType, IMNetwork
from gestorpsi.organization.models import Organization
from gestorpsi.person.models import Person, MaritalStatus, CompanyClient
from gestorpsi.person.forms import CompanyForm, CompanyClientForm
from gestorpsi.person.views import person_save
from gestorpsi.phone.models import PhoneType
from gestorpsi.referral.models import Referral, ReferralChoice, IndicationChoice, Indication, ReferralAttach, REFERRAL_ATTACH_TYPE, Queue, ReferralExternal
from gestorpsi.referral.forms import ReferralForm, ReferralDischargeForm, QueueForm, ReferralExtForm
from gestorpsi.reports.header import header_gen
from gestorpsi.reports.footer import footer_gen
from gestorpsi.util.decorators import permission_required_with_403
from gestorpsi.util.views import get_object_or_None
from gestorpsi.person.views import person_json_list
from gestorpsi.schedule.views import _datetime_view
from gestorpsi.schedule.forms import ScheduleOccurrenceForm
from gestorpsi.schedule.views import add_event
from gestorpsi.schedule.views import occurrence_confirmation_form
from gestorpsi.schedule.forms import OccurrenceConfirmationForm
from gestorpsi.schedule.models import ScheduleOccurrence, Occurrence
from gestorpsi.contact.models import Contact
from gestorpsi.util.views import get_object_or_None
from gestorpsi.util.models import Cnae

# list all active clients
@permission_required_with_403('client.client_list')
def index(request, deactive = False):
    # Test if clinic administrator has registered services before access client page.
    if not Service.objects.filter(active=True, organization=request.user.get_profile().org_active).count():
        return render_to_response('client/client_service_alert.html', context_instance=RequestContext(request))
    return render_to_response('client/client_list.html', locals(), context_instance=RequestContext(request))

# client home
@permission_required_with_403('client.client_read')
def home(request, object_id=None):
    object = get_object_or_404(Client, pk=object_id, person__organization=request.user.get_profile().org_active)
    referrals = Referral.objects.charged().filter(client=object)
    referrals_discharged = Referral.objects.discharged().filter(client=object)

    c=0
    for x in (Referral.objects.filter(client=object)):
        c += x.past_occurrences().count()

    return render_to_response('client/client_home.html',
                                        {
                                        'object': object,
                                        'referrals': referrals,
                                        'referrals_discharged': referrals_discharged,
                                        'service_subscribers': Service.objects.filter(referral__client = object).distinct().count(),
                                        'care_delivered': c,
                    					'clss':request.GET.get('clss')
                                        },
                                        context_instance=RequestContext(request))

@permission_required_with_403('client.client_write')
def add(request):
     #Test if clinic administrator has registered services before access client page.
    if not Service.objects.filter(active=True, organization=request.user.get_profile().org_active).count():
        return render_to_response('client/client_service_alert.html', {'object': _("There's no Service created yet. Please, create one before access Client."), }, context_instance=RequestContext(request))
    else:
        try:
            cities = City.objects.filter(state=request.user.get_profile().org_active.address.all()[0].city.state)
        except:
            cities = {}
        return render_to_response('client/client_form.html',
                                        {
                                        'countries': Country.objects.all(),
                                        'PhoneTypes': PhoneType.objects.all(), 
                                        'AddressTypes': AddressType.objects.all(), 
                                        'EmailTypes': EmailType.objects.all(), 
                                        'IMNetworks': IMNetwork.objects.all() , 
                                        'TypeDocuments': TypeDocument.objects.filter(source=1), 
                                        'Issuers': Issuer.objects.all(), 
                                        'Cities': cities,
                                        'States': State.objects.all(), 
                                        'MaritalStatusTypes': MaritalStatus.objects.all(),
                                        'PROFESSIONAL_AREAS': Profession.objects.all(),
                                        'licenceBoardTypes': LicenceBoard.objects.all(),
                                        'ReferralChoices': ReferralChoice.objects.all(),
                                        'IndicationsChoices': IndicationChoice.objects.all(),
                                        'Relations': Relation.objects.all(),
                                        'cnae': Cnae.objects.all(),
                                         },
                                        context_instance=RequestContext(request))


@permission_required_with_403('client.client_list')
def list(request, page = 1, initial = None, filter = None, no_paging = False, deactive = False):
    user = request.user

    if user.groups.filter(name='administrator') or user.groups.filter(name='secretary'):
        if deactive:
            object = Client.objects.filter(person__organization = user.get_profile().org_active.id, clientStatus = '0').order_by('person__name')
        else:
            object = Client.objects.filter(person__organization = user.get_profile().org_active.id, clientStatus = '1').order_by('person__name')
    else:
        if deactive:
            object = Client.objects.filter(person__organization = user.get_profile().org_active.id, clientStatus = '0', referral__professional = user.profile.person.careprofessional.id).distinct().order_by('person__name')
        else:
            object = Client.objects.filter(person__organization = user.get_profile().org_active.id, clientStatus = '1', referral__professional = user.profile.person.careprofessional.id).distinct().order_by('person__name')

    if initial:
        object = object.filter(person__name__istartswith = initial)

    if filter:
        object = object.filter(person__name__icontains = filter)

    return HttpResponse(simplejson.dumps(person_json_list(request, object, 'client.client_read', page, no_paging), sort_keys=True),
                            mimetype='application/json')

# edit form
@permission_required_with_403('client.client_read')
def form(request, object_id=''):
    object = get_object_or_404(Client, pk=object_id, person__organization=request.user.get_profile().org_active)
    cnae = None
    # User Registration Code
    groups = [False, False, False, False]
    try:
        profile = get_object_or_404(Profile, person=object.person.id)
        for g in profile.user.groups.all():
            if g.name == "administrator": groups[0] = True
            if g.name == "psychologist":  groups[1] = True
            if g.name == "secretary":     groups[2] = True
            if g.name == "client":        groups[3] = True
    except:
        profile = Profile()
        profile.person = get_object_or_404(Person, pk=object.person.id)
        profile.user = User(username=slugify(profile.person.name))
    
    if object.person.is_company():
        template_name = 'client/client_form_company.html'
        company_form = CompanyForm(instance=object.person.company)
        cnae = get_object_or_None(Cnae, pk=object.person.company.cnae_class)
    else:
        template_name = 'client/client_form.html'
        company_form = None

    return render_to_response(template_name,
                              {'object': object,
                                'phones' : object.person.phones.all(),
                                'addresses' : object.person.address.all(),
                                'documents' : object.person.document.all(),
                                'emails' : object.person.emails.all(),
                                'websites' : object.person.sites.all(),
                                'ims' : object.person.instantMessengers.all(),
                                'countries': Country.objects.all(),
                                'PhoneTypes': PhoneType.objects.all(), 
                                'AddressTypes': AddressType.objects.all(), 
                                'EmailTypes': EmailType.objects.all(), 
                                'IMNetworks': IMNetwork.objects.all(), 
                                'TypeDocuments': TypeDocument.objects.filter(source=1), 
                                'Issuers': Issuer.objects.all(), 
                                'States': State.objects.all(), 
                                'MaritalStatusTypes': MaritalStatus.objects.all(), 
                                'PROFESSIONAL_AREAS': Profession.objects.all(),
                                'licenceBoardTypes': LicenceBoard.objects.all(),
                                'ReferralChoices': ReferralChoice.objects.all(),
                                'IndicationsChoices': IndicationChoice.objects.all(),
                                'Relations': Relation.objects.all(),
                                'profile': profile,
                                'groups': groups,
                                'clss': request.GET.get('clss'),
                                'company_form': company_form,
                                'cnae': cnae,
                               },
                              context_instance=RequestContext(request)
                              )

@permission_required_with_403('client.client_read')
def add_company(request, object_id=''):
    object = Client() if not object_id else get_object_or_404(Client, pk=object_id, person__organization=request.user.get_profile().org_active)
    company_form = CompanyForm()

    return render_to_response('client/client_form_company.html',
                              {'object': object,
                                'phones' : None if not object_id else object.person.phones.all(),
                                'addresses' : None if not object_id else object.person.address.all(),
                                'documents' : None if not object_id else object.person.document.all(),
                                'emails' : None if not object_id else object.person.emails.all(),
                                'websites' : None if not object_id else object.person.sites.all(),
                                'ims' : None if not object_id else object.person.instantMessengers.all(),
                                'countries': Country.objects.all(),
                                'PhoneTypes': PhoneType.objects.all(), 
                                'AddressTypes': AddressType.objects.all(), 
                                'EmailTypes': EmailType.objects.all(), 
                                'IMNetworks': IMNetwork.objects.all(), 
                                'TypeDocuments': TypeDocument.objects.filter(source=2), 
                                'Issuers': Issuer.objects.all(), 
                                'States': State.objects.all(), 
                                'Relations': Relation.objects.all(),
                                'company_form': company_form,
                                'cnae': Cnae.objects.all(),
                               },
                              context_instance=RequestContext(request)
                              )

@permission_required_with_403('referral.referral_read')
def referral_plus_form(request, object_id=None, referral_id=None):
    """ This function render a form used by internal referral """
    object = get_object_or_404(Client, pk = object_id, person__organization=request.user.get_profile().org_active)
    data = {'client': [object.id]}

    referral = Referral.objects.get(pk=referral_id, service__organization=request.user.get_profile().org_active)
    #referral_form = ReferralForm(instance=referral)
    referral_form = ReferralForm(data)
    referral_form.fields['professional'].queryset = CareProfessional.objects.filter(active=True, person__organization=request.user.get_profile().org_active)
    referral_form.fields['referral'].queryset = Referral.objects.filter(client=object)
    referral_form.fields['service'].queryset = Service.objects.filter(active=True, organization=request.user.get_profile().org_active)
    referral_form.fields['client'].queryset = Client.objects.filter(person__organization = request.user.get_profile().org_active.id, clientStatus = '1')

    total_service = Referral.objects.filter(client=object).count()
    #referral_list = Referral.objects.filter(client=object, status='01')

    return render_to_response('client/client_referral_plus_form.html',
                              {'object': object, 
                                'referral': referral,
                                'referral_form': referral_form,
                                #'referral_list': referral_list,
                                'referrals': Referral.objects.filter(client = object),
                                'IndicationsChoices': IndicationChoice.objects.all(),
                                'contact_organizations': Contact.objects.filter(
                                                org_id = request.user.get_profile().org_active.id, 
                                                person_id = request.user.get_profile().person.id, 
                                                filter_name = None,
                                                filter_type = 1
                                            ),
                                'contact_professionals': Contact.objects.filter(
                                                org_id = request.user.get_profile().org_active.id, 
                                                person_id = request.user.get_profile().person.id, 
                                                filter_name = None,
                                                filter_type = 2
                                            ),
                               }, context_instance=RequestContext(request))


# add or edit form
@permission_required_with_403('referral.referral_read')
def referral_form(request, object_id = None, referral_id = None):
    object = get_object_or_404(Client, pk = object_id, person__organization=request.user.get_profile().org_active)

    data = {'client': [object.id]}

    try:
        referral = Referral.objects.get(pk=referral_id, service__organization=request.user.get_profile().org_active)
        referral_form = ReferralForm(instance = referral)
        referral_list = None
        referral_form.fields['professional'].queryset = CareProfessional.objects.filter(active=True, person__organization=request.user.get_profile().org_active)
    except:
        # new referral
        referral = ''
        referral_form = ReferralForm(data)

    referral_form.fields['referral'].queryset = Referral.objects.filter(client=object)
    referral_form.fields['service'].queryset = Service.objects.filter(active=True, organization=request.user.get_profile().org_active)
    referral_form.fields['client'].queryset = Client.objects.filter(person__organization = request.user.get_profile().org_active.id, clientStatus = '1')
    total_service = Referral.objects.filter(client=object).count()
    referral_list = Referral.objects.filter(client=object, status='01')

    return render_to_response('client/client_referral_form.html',
                              { 'object': object, 
                                'referral': referral,
                                'referral_form': referral_form,
                                'referral_list': referral_list,
                                'referrals': Referral.objects.filter(client = object),
                                'IndicationsChoices': IndicationChoice.objects.all(),
                                'contact_organizations': Contact.objects.filter(
                                                org_id = request.user.get_profile().org_active.id, 
                                                person_id = request.user.get_profile().person.id, 
                                                filter_name = None,
                                                filter_type = 1
                                            ),
                                'contact_professionals': Contact.objects.filter(
                                                org_id = request.user.get_profile().org_active.id, 
                                                person_id = request.user.get_profile().person.id, 
                                                filter_name = None,
                                                filter_type = 2
                                            ),
                                'AttachTypes': REFERRAL_ATTACH_TYPE,
                               },
                              context_instance=RequestContext(request)
                              )

@permission_required_with_403('referral.referral_write')
def referral_plus_save(request, object_id=None):
    """ This function save an internal referral """
    if request.method == 'POST':
        form = ReferralForm(request.POST)
        if form.is_valid():
            object = form.save(commit=False)
            object.organization = request.user.get_profile().org_active
            object.status = '01'
            object.save()
            form.save_m2m()
        else:
            print form.errors
    request.user.message_set.create(message=_('Referral saved successfully'))

    return HttpResponseRedirect('/client/%s/referral/' % (request.POST.get('client_id')))

""" *** TODO: manage multiples referrals """
@permission_required_with_403('referral.referral_write')
def referral_save(request, object_id = None, referral_id = None):
    if request.method == 'POST':
        try:
            referral = Referral.objects.get(pk=referral_id, service__organization=request.user.get_profile().org_active, referraldischarge__isnull=True)
            form = ReferralForm(request.POST, instance = referral)
        except:
            form = ReferralForm(request.POST)
        if form.is_valid():
            object = form.save(commit=False)
            object.organization = request.user.get_profile().org_active
            object.status = '01'
            if object.service.active:
                object.save()
                ''' just save professionals one time '''
                if not object.professional.all():
                    form.save_m2m()
                ''' Indication  Section '''
                if request.POST.get('indication'):
                    indication = Indication()
                    indication.indication_choice = IndicationChoice.objects.get(pk=request.POST.get('indication'))
                    indication.referral_organization = get_object_or_None(Organization, id=request.POST.get('indication_organization'))
                    indication.referral_professional = get_object_or_None(CareProfessional, id=request.POST.get('indication_professional'))
                    # indication.client = Client.objects.get(pk = object_id)
                    indication.referral = Referral.objects.get(pk = object)
                    indication.save()
                url = '/client/%s/referral/%s/'
                msg = _('Referral saved successfully')
            else:
                url = '/client/%s/referral/%s/?clss=error'
                msg = _('Service is deactive. Impossible register a referral.')
        else:
            return render_to_response('client/client_referral_form.html', locals())

    request.user.message_set.create(message=_(msg))
    return HttpResponseRedirect(url % (object_id, object.id))

@permission_required_with_403('referral.referral_read')
def referral_discharge_form(request, object_id = None, referral_id = None):
    object = get_object_or_404(Client, pk = object_id, person__organization=request.user.get_profile().org_active)
    referral = get_object_or_404(Referral, pk=referral_id, service__organization=request.user.get_profile().org_active)
 
    if referral.on_queue():
        request.user.message_set.create(message=_('Sorry, you can not discharge a queued referral. Remove it from queue first before to continue'))
        return HttpResponseRedirect('/client/%s/referral/%s/?clss=error' % (object.id, referral.id))

    if referral.upcoming_occurrences().count() == 0:
        if request.method == 'POST':
            form = ReferralDischargeForm(request.POST, initial=dict(client=object, referral=referral))
            if form.is_valid():
                data = form.save(commit=False)
                data.client = object
                data.referral = referral
                data.save()

                request.user.message_set.create(message=_('Client discharged successfully'))
                return HttpResponseRedirect('/client/%s/home/' % (object.id))
            else:
                request.user.message_set.create(message=_('Form Error'))
                return render_to_response('client/client_referral_discharge_form.html', locals(), context_instance=RequestContext(request))
        else:
            form = ReferralDischargeForm(initial=dict(client=object, referral=referral))

        return render_to_response('client/client_referral_discharge_form.html', locals(), context_instance=RequestContext(request))

    else:
        request.user.message_set.create(message=_('Registered have hour in the schedule'))
        return HttpResponseRedirect('/client/%s/referral/%s/?clss=error' % (object.id, referral.id))

@permission_required_with_403('referral.referral_list')
def referral_list(request, object_id = None, discharged = None):
    object = get_object_or_404(Client, pk = object_id, person__organization=request.user.get_profile().org_active)

    if discharged:
        referrals = object.referrals_discharged()
    else:
        referrals = object.referrals_charged()
        charged = True

    if request.user.groups.filter(name='professional').count() :
        referrals = referrals.filter(professional = request.user.profile.person.careprofessional.id)

    return render_to_response('client/client_referral_list.html', locals(), context_instance=RequestContext(request))

@permission_required_with_403('referral.referral_read')
def referral_home(request, object_id = None, referral_id = None):
    user = request.user
    object = get_object_or_404(Client, pk = object_id, person__organization=request.user.get_profile().org_active)
    referral = get_object_or_404(Referral, pk=referral_id, service__organization=request.user.get_profile().org_active)
    organization = user.get_profile().org_active.id
    queues = Queue.objects.filter(referral=referral_id)
    referrals = ReferralExternal.objects.filter(referral=referral_id)

    discharged_list = object.referrals_discharged()
    if discharged_list.filter(pk = referral_id).count():
        referral_discharged = True
    else: 
        referral_discharged = False

    clss = request.GET.get("clss")
    dt = referral.date.strftime("%d-%m-%Y  %H:%M ")
    try:
        indication = Indication.objects.get(referral = referral_id)
    except:
        indication = None
    attachs = ReferralAttach.objects.filter(referral = referral_id)

    return render_to_response('client/client_referral_home.html', locals(), context_instance=RequestContext(request))

@permission_required_with_403('client.client_write')
def save(request, object_id=None, is_company = False):
    """
       Save or Update a client record
    """
    user = request.user

    if object_id:
        object = get_object_or_404(Client, pk=object_id, person__organization=request.user.get_profile().org_active)
        person = object.person
    else:
        object = Client()
        person = Person()
        
        # Id Record
        org = get_object_or_404(Organization, pk=user.get_profile().org_active.id )
        object.idRecord = org.last_id_record + 1
        org.last_id_record = org.last_id_record + 1
        org.save()

    object.person = person_save(request, person)
    object.save()
    
    if is_company:
        company_form = CompanyForm(request.POST) if not object_id else CompanyForm(request.POST, instance=object.person.company)
        if not company_form.is_valid():
            print company_form.errors
        else:
            company = company_form.save(commit=False)
            print object.person
            company.person = object.person
            company.save()

    request.user.message_set.create(message=_('Client saved successfully'))

    return HttpResponseRedirect('/client/%s/home' % object.id)

@permission_required_with_403('client.client_list')
def print_list(request):
    user = request.user
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=clients.pdf'
    object = Client.objects.filter(person__organization = user.get_profile().org_active.id, clientStatus = '1').order_by('person__name')
    report = ClientList(queryset=object)
    report.title = "Client List"
    report.band_page_header = header_gen(user.get_profile().org_active)
    report.band_page_footer = footer_gen(user.get_profile().org_active)
    report.generate_by(PDFGenerator, filename=response)
    return response

@permission_required_with_403('client.client_read')
def print_record(request, object_id):
    user = request.user
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=client.pdf'
    client = Client.objects.filter(pk=object_id, person__organization = user.get_profile().org_active.id)
    report = ClientRecord(queryset=client)
    report.title = "Client Record"
    report.band_page_header = header_gen(organization=user.get_profile().org_active, header_line=False, clinic_info=True)
    report.band_page_footer = footer_gen(organization=user.get_profile().org_active)
    report.generate_by(PDFGenerator, filename=response)
    return response

@permission_required_with_403('client.client_read')
def organization_clients(request):
    """
       organization_clients: return json with all clients from logged organization
    """
    user = request.user
    clients = Client.objects.filter(person__organization = user.get_profile().org_active.id, clientStatus = '1', person__name__istartswith=request.GET.get('q') ).order_by('person__name')

    dict = {}
    array = [] #json
    i = 0

    for o in clients:
        c = {
            'id': o.id,
            'name': o.person.name,
        }
        array.append(c)

    dict['results'] = array
    array = simplejson.dumps(dict, encoding = 'iso8859-1')

    return HttpResponse(array, mimetype='application/json')

@permission_required_with_403('client.client_write')
def order(request, object_id = ''):
    object = get_object_or_404(Client, pk = object_id, person__organization=request.user.get_profile().org_active)
    url = '/client/%s/'

    if Referral.objects.charged().filter(client = object).count() == 0:
        if (object.clientStatus == "1" ):
            object.clientStatus  = "0"
            request.user.message_set.create(message=_('User deactivated successfully'))
        else:
            object.clientStatus = "1"
            request.user.message_set.create(message=_('User activated successfully'))
            object.save(force_update=True)

        object.save(force_update=True)
    
    else:
        request.user.message_set.create(message=_('The user have registered referral'))
        url += '?clss=error'
        
    return HttpResponseRedirect(url % object.id)

@permission_required_with_403('schedule.schedule_read')
def schedule_daily(request,
    year = datetime.now().strftime("%Y"), 
    month = datetime.now().strftime("%m"), 
    day = datetime.now().strftime("%d"), 
    template='client/client_schedule_daily.html',
     **params):

    # verify if user has perm
    referral = get_object_or_404(Referral, pk=request.GET.get('referral'), service__organization=request.user.get_profile().org_active)
    
    if referral.on_queue():
        request.user.message_set.create(message=_('Sorry, you can not book a queued client. Remove it first from queue before continue'))
        return HttpResponseRedirect('/client/%s/referral/%s/?clss=error' % (request.GET.get('client'), referral.id))
    
    return _datetime_view(request, template, datetime(int(year), int(month), int(day)), referral = request.GET['referral'], client = request.GET['client'], **params)

@permission_required_with_403('schedule.schedule_write')
def schedule_add(request):

    # verify if user has perm
    get_object_or_404(Referral, pk=request.GET.get('referral'), service__organization=request.user.get_profile().org_active)

    return add_event(request, 
        'client/client_schedule_form.html', 
        event_form_class=ReferralForm,
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
def referral_occurrences(request, object_id = None, referral_id = None, type = 'upcoming'):
    object = get_object_or_404(Client, pk = object_id, person__organization=request.user.get_profile().org_active)
    referral = get_object_or_404(Referral, pk=referral_id, service__organization=request.user.get_profile().org_active)
    occurrences = referral.past_occurrences() if type == 'past' else  referral.upcoming_occurrences()
    
    return render_to_response('client/client_referral_occurrences.html', locals(), context_instance=RequestContext(request))
    
@permission_required_with_403('referral.referral_read')
def referral_queue(request, object_id = '',  referral_id = ''):
    object = get_object_or_404(Client, pk = object_id, person__organization=request.user.get_profile().org_active)
    referral = get_object_or_404(Referral, pk=referral_id, service__organization=request.user.get_profile().org_active)

    if referral.on_queue():
        request.user.message_set.create(message=_('Error adding to queue! Referral is already queued'))
        return HttpResponseRedirect('/client/%s/referral/%s/?clss=error' % (object.id, referral.id))

    if referral.upcoming_occurrences():
        request.user.message_set.create(message=_('Error adding to queue! Referral have upcoming occurrences'))
        return HttpResponseRedirect('/client/%s/referral/%s/?clss=error' % (object.id, referral.id))

    form=QueueForm()
    return render_to_response("client/client_referral_queue.html", locals(), context_instance=RequestContext(request))

@permission_required_with_403('referral.referral_write')
def referral_queue_save(request, object_id = '',  referral_id = ''):
    object = get_object_or_404(Client, pk = object_id, person__organization=request.user.get_profile().org_active)
    referral = get_object_or_404(Referral, pk=referral_id, service__organization=request.user.get_profile().org_active)

    if referral.on_queue():
        request.user.message_set.create(message=_('Error adding to queue! Referral is already queued'))
        return HttpResponseRedirect('/client/%s/referral/%s/?clss=error' % (object.id, referral.id))

    if referral.upcoming_occurrences():
        request.user.message_set.create(message=_('Subscript in the queue not is possible. Referral have upcoming occurrences'))
        return HttpResponseRedirect('/client/%s/referral/%s/?clss=error' % (object.id, referral.id))

    form = QueueForm(request.POST)

    if form.is_valid():
        object_q = Queue()
        object_q = form.save(commit=False)
        object_q.save()
    else:
        print form.errors

    queues = Queue.objects.filter(referral=referral_id)

    request.user.message_set.create(message=_('Referral added to queue successfully'))
    return HttpResponseRedirect('/client/%s/referral/%s/' % (object.id, referral.id))

@permission_required_with_403('referral.referral_write')
def referral_queue_remove(request, object_id = '',  referral_id = '', queue_id = ''):
    """ This action don't remove the register, just save date out of the register """
    object = get_object_or_404(Client, pk = object_id, person__organization=request.user.get_profile().org_active)
    referral = get_object_or_404(Referral, pk=referral_id, service__organization=request.user.get_profile().org_active)
    queue = get_object_or_None(Queue, pk = queue_id)
    
    queue.date_out = datetime.now()
    queue.save()

    queues = Queue.objects.filter(referral=referral_id)

    request.user.message_set.create(message=_('Client removed from queue successfully'))
    return render_to_response('client/client_referral_home.html', locals(), context_instance=RequestContext(request))

@permission_required_with_403('referral.referral_read')
def referral_ext_form(request, object_id ='', referral_id=''):
    object = get_object_or_404(Client, pk = object_id, person__organization=request.user.get_profile().org_active)
    referral = get_object_or_404(Referral, pk=referral_id, service__organization=request.user.get_profile().org_active)

    contact_organizations = Contact.objects.filter(
                                                org_id = request.user.get_profile().org_active.id, 
                                                person_id = request.user.get_profile().person.id, 
                                                filter_name = None,
                                                filter_type = 1
                                                )

    form = ReferralExtForm()
    return render_to_response('client/client_referral_ext.html', locals(), context_instance=RequestContext(request))

@permission_required_with_403('referral.referral_write')
def referral_ext_save(request, object_id = '', referral_id=''):
    object = get_object_or_404(Client, pk = object_id, person__organization=request.user.get_profile().org_active)
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
    else:
        print form.errors

    request.user.message_set.create(message=_('External Referral saved successfully'))
    return render_to_response('client/client_referral_home.html', locals(), context_instance=RequestContext(request))

@permission_required_with_403('client.client_write')
def family(request, object_id = None):
    object = get_object_or_404(Client, pk = object_id, person__organization=request.user.get_profile().org_active)

    if request.method == 'POST':
        form = FamilyForm(request.POST)
        if form.is_valid():
            form.save(request, object)
            request.user.message_set.create(message=_('Family member added successfully'))
            return HttpResponseRedirect('/client/%s/family/' % object.id)
        else:
            return render_to_response('client/client_family.html', locals(), context_instance=RequestContext(request))

    form = FamilyForm()

    return render_to_response('client/client_family.html', locals(), context_instance=RequestContext(request))

@permission_required_with_403('client.client_list')
def company_related(request, object_id = None):
    object = get_object_or_404(Client, pk = object_id, person__organization=request.user.get_profile().org_active)
    clients = CompanyClient.objects.filter(company__person__client = object, company__person__organization=request.user.get_profile().org_active)

    return render_to_response('client/client_company_related.html', locals(), context_instance=RequestContext(request))

@permission_required_with_403('client.client_write')
def company_related_form(request, object_id = None, company_client_id=None):
    object = get_object_or_404(Client, pk = object_id, person__organization=request.user.get_profile().org_active)
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
        if company_client_id:
            form = CompanyClientForm(request.POST, instance=company_client)
        else:
            form = CompanyClientForm(request.POST)
            
        if form.is_valid():
            form.save(request, object)
            request.user.message_set.create(message=_('Related client added successfully to this company'))
            return HttpResponseRedirect('/client/%s/company_clients/' % object.id)
        else:
            return render_to_response('client/client_company_related_form.html', locals(), context_instance=RequestContext(request))

    return render_to_response('client/client_company_related_form.html', locals(), context_instance=RequestContext(request))
