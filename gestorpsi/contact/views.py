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

import operator
from django.utils import simplejson
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.paginator import Paginator
from django.conf import settings
from django.template.defaultfilters import slugify
from django.utils.translation import gettext as _
from gestorpsi.organization.models import Organization
from gestorpsi.phone.models import PhoneType
from gestorpsi.address.models import Country, State, AddressType, City
from gestorpsi.internet.models import EmailType, IMNetwork
from gestorpsi.person.models import Person
from gestorpsi.careprofessional.models import CareProfessional, Profession, ProfessionalIdentification
from gestorpsi.address.views import address_save
from gestorpsi.phone.views import phone_save
from gestorpsi.internet.views import email_save, site_save, im_save
from gestorpsi.util.decorators import permission_required_with_403
from gestorpsi.util.views import get_object_or_None
from gestorpsi.contact.models import Contact

@permission_required_with_403('contact.contact_write')
def extra_data_save(request, object = None):
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
    return object

@permission_required_with_403('contact.contact_list')
def index(request):
    return render_to_response('contact/contact_list.html', context_instance=RequestContext(request))

@permission_required_with_403('contact.contact_list')
def list(request, page = 1, initial = None, filter = None):
    user = request.user
    org = user.get_profile().org_active

    filter_name = None

    if initial:
        filter_name = initial + '%'
        
    if filter:
        filter_name = '%' + filter + '%'

    list = Contact.objects.filter(
        org_id = request.user.get_profile().org_active.id, 
        person_id = user.get_profile().person.id, 
        filter_name = filter_name)

    organizations_count = len(Contact.objects.filter(
        org_id = request.user.get_profile().org_active.id, 
        person_id = user.get_profile().person.id, 
        filter_name = None,
        filter_type = 1
    ))

    professionals_count = len(Contact.objects.filter(
        org_id = request.user.get_profile().org_active.id, 
        person_id = user.get_profile().person.id, 
        filter_name = None,
        filter_type = 2
    ))

    object_length = len(list)
    paginator = Paginator(list, settings.PAGE_RESULTS)
    object = paginator.page(page)

    array = {} #json
    i = 0

    array['util'] = {
        'has_perm_read': user.has_perm('contact.contact_read'),
        'paginator_has_previous': object.has_previous().real,
        'paginator_has_next': object.has_next().real,
        'paginator_previous_page_number': object.previous_page_number().real,
        'paginator_next_page_number': object.next_page_number().real,
        'paginator_actual_page': object.number,
        'paginator_num_pages': paginator.num_pages,
        'object_length': object_length,
        'professionals_length': professionals_count,
        'organizations_length': organizations_count,
    }

    
    array['paginator'] = {}
    for p in paginator.page_range:
        array['paginator'][p] = p
    
    for o in object.object_list:
        array[i] = {
            'id': o.id,
            'name': o.name,
            'email': o.email,
            'phone': o.phone,
            'type': o.type,
            'type_org': o.org_type,
            'organization': o.organization,
            'profession': o.profession,
        }
        i = i + 1

    return HttpResponse(simplejson.dumps(array, sort_keys=True), mimetype='application/json')

def test(request):
    organizations = Organization.objects.filter(contact_owner=request.user.get_profile().person, active=True, visible=True)
    try:
        cities = City.objects.filter(state=request.user.get_profile().org_active.address.all()[0].city.state)
    except:
        cities = {}
    return render_to_response('tags/address_book_organization_mini.html', {
                                    'object': object,
                                    'countries': Country.objects.all(),
                                    'States': State.objects.all(),
                                    'AddressTypes': AddressType.objects.all(),
                                    'PhoneTypes': PhoneType.objects.all(), 
                                    'EmailTypes': EmailType.objects.all(), 
                                    'IMNetworks': IMNetwork.objects.all(),
                                    'organizations': organizations,
                                    'professions': Profession.objects.all(),
                                    'Cities': cities,
                                     },
                                     context_instance=RequestContext(request)
                                     )

@permission_required_with_403('contact.contact_read')
def contact_organization_form(request, object_id = None):
    
    object = get_object_or_None(Organization, pk=object_id) or Organization()
    
    # check if user logged is the owner of actual register
    if object.id and not object.contact_owner == request.user.get_profile().person:
        hide_save_buttom = True

    try:
        Cities = City.objects.filter(state=request.user.get_profile().org_active.address.all()[0].city.state)
    except:
        Cities = {}

    countries = Country.objects.all()
    States = State.objects.all()
    AddressTypes = AddressType.objects.all()
    PhoneTypes = PhoneType.objects.all() 
    EmailTypes = EmailType.objects.all() 
    IMNetworks = IMNetwork.objects.all()

    phones    = object.phones.all()
    addresses = object.address.all()
    emails    = object.emails.all()
    websites     = object.sites.all()
    ims = object.instantMessengers.all()

    return render_to_response('contact/contact_organization_form.html', locals(),
                                     context_instance=RequestContext(request)
                                     )

@permission_required_with_403('contact.contact_read')
def contact_professional_form(request, object_id = None):
    object = get_object_or_None(CareProfessional, pk=object_id) or CareProfessional()
    organizations = Organization.objects.filter(contact_owner=request.user.get_profile().person, active=True, visible=True)

    # check if user is the owner of the register 
    if object.id and not object.revision().user == request.user:
        hide_save_buttom = True

    if object_id:
        phones    = object.person.phones.all()
        addresses = object.person.address.all()
        emails    = object.person.emails.all()
        websites     = object.person.sites.all()
        ims = object.person.instantMessengers.all()

    countries = Country.objects.all()
    States = State.objects.all()
    AddressTypes = AddressType.objects.all()
    PhoneTypes = PhoneType.objects.all() 
    EmailTypes = EmailType.objects.all() 
    IMNetworks = IMNetwork.objects.all()
    professions = Profession.objects.all()

    try:
        Cities = City.objects.filter(state=request.user.get_profile().org_active.address.all()[0].city.state)
    except:
        Cities = {}
    
    return render_to_response('contact/contact_professional_form.html', locals(),
                                     context_instance=RequestContext(request)
                                     )

@permission_required_with_403('contact.contact_write')
def contact_organization_save(request, object_id = None):
    object = get_object_or_None(Organization, pk=object_id) or Organization()
    
    # check if user is the owner of the register
    if object.id and not object.contact_owner == request.user.get_profile().person:
        return render_to_response('403.html', {'object': _("Access Denied"), }, context_instance=RequestContext(request))

    if not request.POST.get('name'):
        return HttpResponseRedirect(('/contact/form/organization/' if not object.id else ('/contact/form/organization/%s/') % object.id ))

    object.name = request.POST.get('name')
    object.short_name = slugify(object.name)
    object.organization = request.user.get_profile().org_active
    object.contact_owner = request.user.get_profile().person

    object.save()

    object = extra_data_save(request, object)
    request.user.message_set.create(message=_('Organization contact saved successfully'))
    return HttpResponseRedirect('/contact/form/organization/%s/' % (object.id))

@permission_required_with_403('contact.contact_write')
def contact_professional_save(request, object_id = None):

    try:
        object = get_object_or_404(CareProfessional, pk=object_id)
        identification = object.professionalIdentification
        person = object.person
    except:
        object = CareProfessional()
        person = Person()
    
    # check if user is the owner of the register 
    if object.id and not object.revision().user == request.user:
        return render_to_response('403.html', {'object': _("Access Denied"), }, context_instance=RequestContext(request))

    if not request.POST.get('name'):
        return HttpResponseRedirect(('/contact/form/professional/' if not object.id else ('/contact/form/professional/%s/') % object.id ))

    if request.POST.get('symbol'): 
        identification = ProfessionalIdentification()
        identification.profession = Profession.objects.get(id=request.POST.get('symbol'))
        identification.registerNumber = request.POST.get('professional_subscription')
        identification.save()
        object.professionalIdentification = identification

    person.name = request.POST.get('name')
    person.save()

    person.organization.remove()
    person.organization.add(Organization.objects.get(pk=request.POST.get('organization')))

    person = extra_data_save(request, person)

    object.person = person
    object.save()
    
    request.user.message_set.create(message=_('Professional contact saved successfully'))
    return HttpResponseRedirect('/contact/form/professional/%s/' % (object.id))

@permission_required_with_403('contact.contact_write')
def save_mini(request):
    user = request.user
    object = Organization()
    object.name = request.POST.get('label') # adding by mini form
    object.short_name = slugify(request.POST.get('label'))
    object.organization = user.get_profile().org_active
    object.contact_owner = user.get_profile().person
    object.save()

    return HttpResponse("%s" % (object.id))

@permission_required_with_403('contact.contact_write')
def contact_organization_order(request, object_id = None):
    object = get_object_or_None(Organization, pk=object_id) or Organization()

    if object.active == True:
        object.active = False
    else:
        object.active = True

    object.save(force_update=True)
    return HttpResponseRedirect('/contact/form/organization/%s/' % (object.id))

@permission_required_with_403('contact.contact_write')
def contact_professional_order(request, object_id = None):
    object = get_object_or_None(CareProfessional, pk=object_id) or CareProfessional()

    if object.active == True:
        object.active = False
    else:
        object.active = True

    object.save(force_update=True)
    return HttpResponseRedirect('/contact/form/professional/%s/' % (object.id))
