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
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson
from django.utils.html import strip_tags
from django.template.defaultfilters import slugify
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from gestorpsi.settings import DEBUG, MEDIA_URL, MEDIA_ROOT, PAGE_RESULTS
from gestorpsi.address.models import Country, State, AddressType, City
from gestorpsi.authentication.models import Profile
from gestorpsi.careprofessional.models import LicenceBoard, CareProfessional
from gestorpsi.service.models import Service, ServiceGroup, GroupMembers
from gestorpsi.careprofessional.models import CareProfessional
from gestorpsi.careprofessional.views import Profession
from gestorpsi.client.models import Client, Relation
from gestorpsi.client.forms import FamilyForm
from gestorpsi.document.models import TypeDocument, Issuer
from gestorpsi.contact.models import EmailType, IMNetwork
from gestorpsi.organization.models import Organization
from gestorpsi.person.models import Person, MaritalStatus, CompanyClient
from gestorpsi.person.forms import CompanyForm, CompanyClientForm, PersonForm
from gestorpsi.person.helpers import person_save
from gestorpsi.contact.models import PhoneType
from gestorpsi.referral.models import Referral, ReferralChoice, IndicationChoice, Indication, ReferralAttach, REFERRAL_ATTACH_TYPE, Queue, ReferralExternal, ReferralDischarge
from gestorpsi.admission.models import ReferralChoice as AdmissionChoice, AdmissionReferral
from gestorpsi.referral.forms import ReferralForm, ReferralDischargeForm, QueueForm, ReferralExtForm
from gestorpsi.referral.views import _referral_view
from gestorpsi.referral.views import _referral_occurrences
#from gestorpsi.reports.header import header_gen
#from gestorpsi.reports.footer import footer_gen
from gestorpsi.util.decorators import permission_required_with_403
from gestorpsi.util.views import get_object_or_None
from gestorpsi.person.helpers import person_json_list
from gestorpsi.schedule.views import _datetime_view
from gestorpsi.schedule.forms import ScheduleOccurrenceForm
from gestorpsi.schedule.views import add_event
from gestorpsi.schedule.views import occurrence_confirmation_form
from gestorpsi.schedule.forms import OccurrenceConfirmationForm
from gestorpsi.schedule.models import ScheduleOccurrence, Occurrence
from gestorpsi.contact.models import Contact
from gestorpsi.util.views import get_object_or_None, write_pdf
from gestorpsi.util.models import Cnae
from gestorpsi.ehr.views import _access_ehr_check_read
from gestorpsi.address.views import address_save
from gestorpsi.document.views import document_save
from gestorpsi.person.models import MaritalStatus
from gestorpsi.contact.helpers import phone_save, email_save, site_save, im_save
from gestorpsi import settings 


def _access_check(request, object=None):
    """
    client read rights
    this method checks if logged professional have rights to read client data
    @object: client
    """
        
    # check if user is professional and not admin or secretary. 
    if request.user.groups.filter(name='administrator') or request.user.groups.filter(name='secretary'):
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

    # check if user is professional and not admin or secretary. if it's true, check if professional has referral with this customer
    if request.user.groups.filter(name='administrator') or request.user.groups.filter(name='secretary'):
        return True

    # check if professional
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