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

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.utils.translation import gettext as _
from django.contrib import messages
from gestorpsi.address.models import Country, State, AddressType
from gestorpsi.phone.models import PhoneType
from gestorpsi.internet.models import EmailType, IMNetwork
from gestorpsi.document.models import TypeDocument, Issuer
from gestorpsi.person.models import MaritalStatus
from gestorpsi.person.views import person_save
from gestorpsi.careprofessional.models import CareProfessional, Profession, Availability
from gestorpsi.organization.models import Agreement
from gestorpsi.place.models import Place, PlaceType
from gestorpsi.service.models import Service
from gestorpsi.careprofessional.views import save_careprof
from datetime import time

def form(request):
    try:
        object = request.user.get_profile()
    except:
        raise Http404

    countries = Country.objects.all()
    PhoneTypes = PhoneType.objects.all()
    AddressTypes = AddressType.objects.all()
    EmailTypes = EmailType.objects.all()
    IMNetworks = IMNetwork.objects.all()
    TypeDocuments = TypeDocument.objects.all()
    Issuers = Issuer.objects.all()
    States = State.objects.all()
    MaritalStatusTypes = MaritalStatus.objects.all()

    phones    = object.person.phones.all()
    addresses = object.person.address.all()
    documents = object.person.document.all()
    emails    = object.person.emails.all()
    websites  = object.person.sites.all()
    ims       = object.person.instantMessengers.all()

    return render_to_response('profile/profile_person.html', locals(), context_instance=RequestContext(request))

def form_careprofessional(request):
    object = get_object_or_404(CareProfessional, pk=request.user.get_profile().person.careprofessional.id)
    workplaces = object.professionalProfile.workplace.all()
    agreements = object.professionalProfile.agreement.all()

    return render_to_response('profile/profile_careprofessional.html', {
                                    'object': object,
                                    'PROFESSIONAL_AREAS': Profession.objects.all(),
                                    'AgreementTypes': Agreement.objects.all(),
                                    'WorkPlacesTypes': Place.objects.filter(organization = request.user.get_profile().org_active.id),
                                    'workplaces': workplaces,
                                    'agreements': agreements,
                                    'ServiceTypes': Service.objects.filter( active=True, organization=request.user.get_profile().org_active ),
                                    'PlaceTypes': PlaceType.objects.all(),
                                    },
                              context_instance=RequestContext(request))

def save(request):
    if not request.method == 'POST':
        raise Http404
    try:
        person = request.user.get_profile().person
        person_save(request, person)
    except:
        raise Http404

    messages.success(request, _('Profile updated successfully'))
    return HttpResponseRedirect('/profile/')

def save_careprofessional(request):
    object = get_object_or_404(CareProfessional, pk=request.user.get_profile().person.careprofessional.id)
    object = save_careprof(request, object.id, False)
    messages.success(request, _('Professional profile saved successfully'))
    return HttpResponseRedirect('/profile/careprofessional/')

def change_pass(request):
    #if request.user.get_profile().person.is_careprofessional:
        #object = get_object_or_404(CareProfessional, pk=request.user.get_profile().person.careprofessional.id)
    #if request.user.get_profile().person.is_careprofessional:
        #object = get_object_or_404(CareProfessional, pk=request.user.get_profile().person.careprofessional.id)

    clss = request.GET.get("clss")

    if request.POST.get('c_pass'):
        if not request.user.check_password(request.POST.get("c_pass")):
            messages.success(request, _('The current password is wrong'))
            return HttpResponseRedirect('/profile/chpass/?clss=error')
        else:
            if request.POST.get("n_pass") != request.POST.get("n_pass0"):
                messages.success(request, _('The confirmation of the new password is wrong'))
                return HttpResponseRedirect('/profile/chpass/?clss=error')
            else:
                request.user.set_password(request.POST.get('n_pass'))
                request.user.get_profile().temp = request.POST.get('n_pass')    # temporary field (LDAP)
                request.user.get_profile().save(force_update=True)
                request.user.save(force_update=True)
                messages.success(request, _('Password updated successfully'))
                return HttpResponseRedirect('/profile/chpass')
    else:
        return render_to_response('profile/profile_change_pass.html', locals(), context_instance=RequestContext(request))

def add_availability(request):
    days_of_week = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday')
    hours = range(8,18)

    object = get_object_or_404(CareProfessional, pk=request.user.get_profile().person.careprofessional.id)

    for day in days_of_week:
        if request.POST.getlist(day):
            times_of_day = request.POST.getlist(day)

            for hour in times_of_day:
                availability = Availability.objects.get(day=day, hour=time(int(hour)))

                if not availability:
                    availability = Availability(day=day, hour=time(int(hour)))
                    availability.save()

                object.availability.add(availability)
                object = save_careprof(request, object.id, False)


    if request.POST:
        messages.success(request, _('Availability updated successfully!'))

        return render_to_response('profile/profile_add_availability.html',
            {'days_of_week': days_of_week, 'hours': hours}, context_instance=RequestContext(request))
    else:
        return render_to_response('profile/profile_add_availability.html',
            {'days_of_week': days_of_week, 'hours': hours}, context_instance=RequestContext(request))
