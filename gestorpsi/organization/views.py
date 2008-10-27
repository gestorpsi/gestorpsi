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

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from gestorpsi.organization.models import Organization
from gestorpsi.phone.models import Phone, PhoneType
from gestorpsi.address.models import Country, City, State, Address, AddressType
from gestorpsi.internet.models import Email, EmailType, InstantMessenger, IMNetwork
from gestorpsi.address.views import address_save
from gestorpsi.phone.views import phone_save
from gestorpsi.internet.views import email_save, site_save, im_save

def form(request):
    user = request.user
    return render_to_response('organization/organization_form.html', {
        'object': Organization.objects.get(pk= user.org_active.id),
        'PhoneTypes': PhoneType.objects.all(), 
        'AddressTypes': AddressType.objects.all(), 
        'EmailTypes': EmailType.objects.all(), 
        'IMNetworks': IMNetwork.objects.all(),
        'countries': Country.objects.all(),
        'States': State.objects.all(),
        })

def save(request, object_id):
    user = request.user
    object = get_object_or_404( Organization, pk=object_id )

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

    return HttpResponse("Clinica: (%s) %s" % (object_id, object))






