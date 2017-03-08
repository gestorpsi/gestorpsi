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
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.core.paginator import Paginator
from django.conf import settings
from django.template.defaultfilters import slugify
from django.utils.translation import gettext as _
from django.contrib import messages
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

def have_organization_perms_save(request, object):
    if  object.organization != request.user.get_profile().org_active \
        or ( not object.revision_created().user == request.user \
        and 'administrator' not in [ g.name for g in request.user.groups.all()] \
        and 'secretary' not in [ g.name for g in request.user.groups.all()]):
        return False
    else:
        return True

def have_careprofessional_perms_save(request, object):
    if  request.user.get_profile().org_active not in [ i.organization for i in object.person.organization.all()] \
        or ( not object.revision_created().user == request.user \
        and 'administrator' not in [ g.name for g in request.user.groups.all()] \
        and 'secretary' not in [ g.name for g in request.user.groups.all()]):
        return False
    else:
        return True

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
def index(request, deactive = False, template='contact/contact_list.html'):
    return render_to_response(template, locals(), context_instance=RequestContext(request))

@permission_required_with_403('contact.contact_list')
def list(request, page = 1, initial = None, filter = None, deactive=False, filter_type='internal'):
    user = request.user
    org = user.get_profile().org_active

    filter_name = None

    if initial:
        filter_name = initial + '%'
        
    if filter:
        filter_name = '%' + filter + '%'

    if filter_type == 'internal':
        search_method = Contact.objects.filter_internal
    elif filter_type == 'external':
        search_method = Contact.objects.filter_external
    else:
        search_method = Contact.objects.filter

    list = search_method(
        org_id = request.user.get_profile().org_active.id, 
        filter_name = filter_name,
        deactive=deactive,
        )

    organizations_count = len(search_method(
        org_id = request.user.get_profile().org_active.id, 
        filter_name = None,
        filter_type = 1,
        deactive=deactive,
    ))

    professionals_count = len(search_method(
        org_id = request.user.get_profile().org_active.id, 
        filter_name = None,
        filter_type = 2,
        deactive=deactive,
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

@permission_required_with_403('contact.contact_write')
def contact_organization_form(request, object_id = None):
    object = get_object_or_None(Organization, pk=object_id) or Organization()

    if object.id: # register already exists. let's check access permissions
        if object.is_local(): # local contact, only visible for users from the same organization
            if object.organization != request.user.get_profile().org_active:
                raise Http404
        else: # real organization. access allowed only if it has been set to Visible
            if not object.visible: # organization set to NOT visible
                    raise Http404

        # check if user will have permission to save it, and pass it to template
        if not have_organization_perms_save(request, object):
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

    clss = request.GET.get('clss')

    return render_to_response('contact/contact_organization_form.html', locals(),
                                     context_instance=RequestContext(request)
                                     )

@permission_required_with_403('contact.contact_write')
def contact_professional_form(request, object_id = None):
    object = get_object_or_None(CareProfessional, pk=object_id) or CareProfessional()
    organizations = Organization.objects.filter(organization=request.user.get_profile().org_active, visible=True)
    if object.active:
        organizations = organizations.filter(active=True)

    if object.id: # register already exists. let's check access permissions
        if not False in [o.is_local() for o in object.person.organization.all()]: # POSSIBLE local contact, only visible for users from the same organization
            if request.user.get_profile().org_active not in [ i.organization for i in object.person.organization.all()]:
                raise Http404
        else: # POSSIBLE real organization. access allowed only if it has been set to Visible
            if False in [o.visible for o in object.person.organization.all()]:
                raise Http404

        # check if user will have permission to save it, and pass it to template
        if not have_careprofessional_perms_save(request, object):
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

    # check if user is the owner of the register or have admistration profile
    if object.id and not have_organization_perms_save(request, object):
        return render_to_response('403.html', {'object': _("Access Denied"), }, context_instance=RequestContext(request))

    if not request.POST.get('name'):
        return HttpResponseRedirect(('/contact/form/organization/' if not object.id else ('/contact/form/organization/%s/') % object.id ))

    object.name = request.POST.get('name')
    object.short_name = slugify(object.name)
    object.organization = request.user.get_profile().org_active
    object.contact_owner = request.user.get_profile().person
    object.comment = request.POST.get('comments')

    from django.db import IntegrityError
    try:
        object.save()
    except IntegrityError:
        from django.db import connection
        connection.close()
        messages.success(request, _('This organization has already been registered'))
        return HttpResponseRedirect('/contact/form/organization/?clss=error')

    object = extra_data_save(request, object)
    
    messages.success(request, _('Organization contact saved successfully'))
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

    if object.id and not have_careprofessional_perms_save(request, object):
        return render_to_response('403.html', {'object': _("Access Denied"), }, context_instance=RequestContext(request))

    if not request.POST.get('name'):
        return HttpResponseRedirect(('/contact/form/professional/' if not object.id else ('/contact/form/professional/%s/') % object.id ))

    if not object.professionalIdentification:
        if request.POST.get('symbol'): 
            identification = ProfessionalIdentification()
            identification.profession = Profession.objects.get(id=request.POST.get('service_profession'))
            identification.registerNumber = request.POST.get('professional_subscription')
            identification.save()
            object.professionalIdentification = identification
        else:
            object.professionalIdentification = None

    person.name = request.POST.get('name')
    person.save()

    person.organization.remove()
    person.organization.add(Organization.objects.get(pk=request.POST.get('organization')))

    person = extra_data_save(request, person)
    
    object.comments = request.POST.get('comments')
    object.person = person
    object.save()
    
    messages.success(request, _('Professional contact saved successfully'))
    return HttpResponseRedirect('/contact/form/professional/%s/' % (object.id))



'''
    save organization as contact
    short_name field is unique, return 0, don't save
    return array: [0] = True or False / exsit or not
                  [1] = id
                  [2] = name
                  to append in select.
'''
@permission_required_with_403('contact.contact_write')
def save_mini(request):

    user = request.user
    obj = Organization()

    if request.POST.get('label'):
        if Organization.objects.filter(short_name=slugify(request.POST.get('label')) ):
            r = True
        else:
            obj.name = request.POST.get('label') # adding by mini form
            obj.short_name = slugify(request.POST.get('label'))
            obj.organization = user.get_profile().org_active
            obj.contact_owner = user.get_profile().person
            obj.save()
            r = u"%s|%s|%s" % (False, obj.id, obj.name)

    return HttpResponse(r)



@permission_required_with_403('contact.contact_write')
def save_mini_professional(request):
    object = CareProfessional()
    person = Person()
    person.name = request.POST.get('label')
    person.save()
    person.organization.add(Organization.objects.get(pk=request.POST.get('organization')))
    object.person = person
    object.save()

    return HttpResponse("%s" % (object.id))

@permission_required_with_403('contact.contact_write')
def contact_organization_order(request, object_id = None):
    object = get_object_or_404(Organization, pk=object_id, organization=request.user.get_profile().org_active)

    # check if user is the owner of the register or have admistration profile
    if not have_organization_perms_save(request, object):
        return render_to_response('403.html', {'object': _("Access Denied"), }, context_instance=RequestContext(request))

    if object.active == True:
        object.active = False
        for p in CareProfessional.objects.filter(person__organization=object):
            p.active = False
            p.save()
    else:
        object.active = True

    object.save(force_update=True)

    messages.success(request, ('%s' % (_('Contact activated successfully') if object.active else _('Contact deactivated successfully'))))
    return HttpResponseRedirect('/contact/form/organization/%s/' % (object.id))

@permission_required_with_403('contact.contact_write')
def contact_professional_order(request, object_id = None):
    object = get_object_or_404(CareProfessional, pk=object_id, person__organization__organization=request.user.get_profile().org_active)

    # check if user is the owner of the register or have admistration profile
    if not have_careprofessional_perms_save(request, object):
        return render_to_response('403.html', {'object': _("Access Denied"), }, context_instance=RequestContext(request))

    if object.active == True:
        object.active = False
    else:
        object.active = True
        for o in object.person.organization.all():
            if not o.active:
                o.active = True
                o.save()

    object.save(force_update=True)

    messages.success(request, ('%s' % (_('Contact activated successfully') if object.active else _('Contact deactivated successfully'))))
    return HttpResponseRedirect('/contact/form/professional/%s/' % (object.id))
