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
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from django.contrib import messages
from gestorpsi.organization.models import PersonType, UnitType, AdministrationEnvironment, Source, ProvidedType, Management, Dependence, Activitie, Organization, ProfessionalResponsible, TIME_SLOT_SCHEDULE
from gestorpsi.phone.models import PhoneType
from gestorpsi.address.models import Country, State, AddressType
from gestorpsi.internet.models import EmailType, IMNetwork
from gestorpsi.address.views import address_save
from gestorpsi.phone.views import phone_save
from gestorpsi.internet.views import email_save, site_save, im_save
from gestorpsi.util.decorators import permission_required_with_403
from gestorpsi.careprofessional.models import Profession, CareProfessional
from gestorpsi.util.views import get_object_or_None

from gestorpsi.gcm.models import Invoice, INVOICE_STATUS_CHOICES
from gestorpsi.gcm.models.plan import Plan
from gestorpsi.gcm.models.payment import PaymentType

from datetime import datetime, timedelta
from gestorpsi.boleto.functions import gera_boleto_bradesco
from gestorpsi.boleto.models import BradescoBilletData


@permission_required_with_403('organization.organization_write')
def professional_responsible_save(request, object, ids, names, subscriptions, organization_subscriptions, professions):

    ProfessionalResponsible.objects.filter(organization=object).delete()

    # required
    if range(len(names)) > 0 :
        for x in range(len(names)):
            obj = []

            # Whitout Profession of the Professional
            if not professions[x]:
                if names[x]:
                    obj = (ProfessionalResponsible(name=names[x], subscription=subscriptions[x], organization=object, organization_subscription=organization_subscriptions[x] ))
            else:
                # Whit Profession of the Professional
                if names[x]:
                    obj = (ProfessionalResponsible(name=names[x], subscription=subscriptions[x], organization=object, organization_subscription=organization_subscriptions[x], profession=get_object_or_None(Profession, pk=professions[x])))

            if ( len(names[x]) != 0 or len(subscriptions[x]) !=0 ):
                obj.save()



@permission_required_with_403('organization.organization_read')
def form(request):

    user = request.user
    object = get_object_or_404( Organization, pk=user.get_profile().org_active.id )

    return render_to_response('organization/organization_form.html', {
        'object': object, #Organization.objects.get(pk= user.get_profile().org_active.id),
        'PhoneTypes': PhoneType.objects.all(), 
        'AddressTypes': AddressType.objects.all(), 
        'EmailTypes': EmailType.objects.all(), 
        'IMNetworks': IMNetwork.objects.all(),
        'countries': Country.objects.all(),
        'States': State.objects.all(),
        'phones': object.phones.all(),
        'addresses': object.address.all(),
        'emails': object.emails.all(),
        'websites': object.sites.all(),
        'ims': object.instantMessengers.all(),
        'PersonType': PersonType.objects.all(),
        'UnitType': UnitType.objects.all(),
        'AdministrationEnvironment': AdministrationEnvironment.objects.all(),
        'Source': Source.objects.all(),
        'ProvidedType': ProvidedType.objects.all(),
        'Management': Management.objects.all(),
        'Dependence': Dependence.objects.all(),
        'Activitie': Activitie.objects.all(),
        'professional_responsible': ProfessionalResponsible.objects.filter(organization = user.get_profile().org_active),
        'Professions': Profession.objects.all(),
        'time_slot_schedule': TIME_SLOT_SCHEDULE,
        },
        context_instance=RequestContext(request))


@permission_required_with_403('organization.organization_write')
def make_second_copy(request, invoice):
    user = request.user

    invoice = Invoice.objects.get(pk=invoice)
    aux = Invoice.objects.filter(status=1, organization=invoice.organization, due_date__gt=datetime.now()).count()
    if aux <= 0:
        inv = Invoice()
        inv.organization = invoice.organization
        inv.due_date = datetime.now() + timedelta(days=7)
        inv.expiry_date = invoice.expiry_date
        inv.ammount = invoice.ammount
        inv.discount = invoice.discount
        inv.status = 1
        inv.plan = invoice.plan
        inv.save()
        
        invoice.status = 3
        invoice.save()
        
        data = BradescoBilletData.objects.all()[0]
        billet_url = gera_boleto_bradesco(request.user.id, inv, days=data.default_second_copy_days, second_copy=True)
        inv.billet_url = billet_url
        inv.save()
        aux = True
        message = 'Second copy details saved successfully'
    else:
        message = 'Second copy not generated: there are billets that still requiring payment.'
        aux = False 
        
    return render_to_response('organization/second_copy.html', locals(), context_instance=RequestContext(request))


@permission_required_with_403('organization.organization_write')
def save(request):

    user = request.user

    try:
        object = Organization.objects.get(pk= user.get_profile().org_active.id)
    except:
        object = Organization()
        object.short_name = slugify(request.POST['name'])
    
    if (object.short_name != request.POST['short_name']):
        if (Organization.objects.filter(short_name__iexact = request.POST['short_name']).count()):
            return HttpResponse("false")
        else:
            object.short_name = request.POST['short_name']
    
    #identity
    object.name = request.POST['name']
    object.trade_name = request.POST['trade_name']
    object.register_number = request.POST['register_number']
    object.cnes = request.POST['cnes']
    object.state_inscription = request.POST.get('state_inscription')
    object.city_inscription = request.POST['city_inscription']
    object.photo = request.POST['photo']
    object.visible = get_visible( request, request.POST.get('visible') )
    #profile
    object.person_type = get_object_or_None(PersonType, pk=request.POST.get('person_type'))
    object.unit_type = get_object_or_None(UnitType, pk=request.POST.get('unit_type'))
    object.environment = get_object_or_None(AdministrationEnvironment, pk=request.POST.get('environment'))
    object.management = get_object_or_None(Management, pk=request.POST.get('management'))
    object.source = get_object_or_None(Source, pk=request.POST.get('source'))
    object.dependence = get_object_or_None(Dependence, pk=request.POST.get('dependence'))
    object.activity = get_object_or_None(Activitie, pk=request.POST.get('activity'))
    """ provided types """
    object.provided_type.clear()
    object.time_slot_schedule = request.POST.get('time_slot_schedule')

    for p in request.POST.getlist('provided_type'):
        object.provided_type.add(ProvidedType.objects.get(pk=p))

    object.comment = request.POST['comment']
    object.save()
   
    professional_responsible_save(request, object, request.POST.getlist('professionalId'), request.POST.getlist('professional_name'), request.POST.getlist('professional_subscription'), request.POST.getlist('professional_organization_subscription'), request.POST.getlist('service_profession'))

    phone_save(object, request.POST.getlist('phoneId'), request.POST.getlist('area'), request.POST.getlist('phoneNumber'), request.POST.getlist('ext'), request.POST.getlist('phoneType'))
    email_save(object, request.POST.getlist('email_id'), request.POST.getlist('email_email'), request.POST.getlist('email_type'))
    site_save(object, request.POST.getlist('site_id'), request.POST.getlist('site_description'), request.POST.getlist('site_site'))
    im_save(object, request.POST.getlist('im_id'), request.POST.getlist('im_identity'), request.POST.getlist('im_network'))
    address_save(object, request.POST.getlist('addressId'), request.POST.getlist('addressPrefix'),
    request.POST.getlist('addressLine1'), request.POST.getlist('addressLine2'),
    request.POST.getlist('addressNumber'), request.POST.getlist('neighborhood'),
    request.POST.getlist('zipCode'), request.POST.getlist('addressType'),
    request.POST.getlist('city'), request.POST.getlist('foreignCountry'),
    request.POST.getlist('foreignState'), request.POST.getlist('foreignCity'))

    messages.success(request, _('Organization details saved successfully'))
    return HttpResponseRedirect('/organization/')
    

'''
    Tiago de Souza Moraes 20/06/2014
    Organization short name is available?
    return 0=No / 1=Yes
'''
@permission_required_with_403('organization.organization_read')
def shortname_is_available(request, short):
    if Organization.objects.filter(short_name__iexact = short).count():
	    return HttpResponse("0")
    else:
	    return HttpResponse("1")



def get_visible( request, value ):
    if ( value == 'on' ):
        return True
    else:
        return False 



def list_prof_org(request, org_id = None):
    org = Organization.objects.get(pk = org_id)
    list = CareProfessional.objects.filter(person__organization = org, active=True, person__organization__visible = True)

    i = 0
    array = {} #JSON
    for o in list:
        array[i] = {
                'name': '%s' % o,
                'id': o.id,
                }
        i = i + 1

    return HttpResponse(simplejson.dumps(array), mimetype='application/json')



'''
    organization signature save
    Tiago de Souza Moraes 20/06/2014
'''
#@permission_required_with_403('organization.organization_write')
def signature_save(request):

    user = request.user
    obj = Organization.objects.get(pk= user.get_profile().org_active.id) # get org from logged user

    if request.POST:

        obj.prefered_plan = get_object_or_None(Plan, pk=request.POST.get('prefered_plan'))
        obj.payment_type = PaymentType.objects.get( pk=request.POST.get('payment_type') )
        obj.save()

        messages.success(request, _('Organization details saved successfully'))
        return HttpResponseRedirect('/organization/signature/')

    else:

        return render_to_response('organization/organization_signature.html', {
            'obj': obj,
            'plans': Plan.objects.filter( active=True ).order_by('weight'),
            'invoices': Invoice.objects.filter(organization=object, status=1).order_by('date'), 
            'payment_type': PaymentType.objects.filter(active=True, show_to_client=True).order_by('-name'),
            },
            context_instance=RequestContext(request))


"""
    suspension signature of organization
    register reason to suspension organization
"""
def suspension(request):

    obj = Organization.objects.get(pk=request.user.get_profile().org_active.id) # get org from logged user

    if request.POST and request.POST.get('suspension_confirm'):

        r = u"Conta suspensa dia %s\n\n" %  datetime.today().strftime("%d %B %Y, %H:%m")
        for x in request.POST.getlist('suspension_reason'):
            r += u"%s\n\n" % x

        if request.POST.get('other_reason'):
            r += request.POST.get('other_reason')

        obj.suspension = True
        obj.suspension_reason = r
        obj.save()

        messages.success(request, _('Organization details saved successfully') )
        return HttpResponseRedirect('/organization/suspension/')

    else:
        return render_to_response('organization/organization_signature_suspension.html', {
            'obj': obj,
            },
            context_instance=RequestContext(request))
