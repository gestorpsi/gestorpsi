#-*- coding: utf-8 -*-

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
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext as _
from django.template.context import RequestContext
from django.contrib import messages
from gestorpsi.person.models import Person
from gestorpsi.client.models import Client
from gestorpsi.organization.models import Organization
from gestorpsi.careprofessional.models import LicenceBoard, CareProfessional
from gestorpsi.admission.models import *
from gestorpsi.contact.models import Contact
from gestorpsi.util.views import get_object_or_None
from gestorpsi.util.decorators import permission_required_with_403
from django.conf import settings
import os
import uuid
from gestorpsi.client.views import _access_check

@permission_required_with_403('admission.admission_read')
def form(request, object_id=''):
    object = get_object_or_404(Client, pk=object_id, person__organization=request.user.get_profile().org_active)

    # check access by requested user
    if not _access_check(request, object):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    attachs = Attach.objects.filter(client = object)

    return render_to_response('admission/admission_form.html', {
        'object': object,
        'types': ATTACH_TYPE,
        'attachs': attachs,
        'org_id': request.user.get_profile().org_active.id,
        'contact_organizations':  Contact.objects.filter_internal(
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
        'contact_organizations_external':  Contact.objects.filter_external(
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
        'ReferralChoices': ReferralChoice.objects.all(),
    }, context_instance=RequestContext(request))

@permission_required_with_403('admission.admission_read')
def is_responsible(value):
    if (value == 'on'):
        return True
    else:
        return False

@permission_required_with_403('admission.admission_write')
def save(request, object_id=''):
    object = get_object_or_404(Client, pk=object_id, person__organization=request.user.get_profile().org_active)

    # check access by requested user
    if not _access_check(request, object):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    object.admission_date = datetime.strptime(request.POST.get('admission_date'), '%d/%m/%Y')
    object.legacyRecord = request.POST.get('legacyRecord')
    object.comments = request.POST.get('comments')

    object.admissionreferral_set.all().delete()
    """ Referral Section """
    if request.POST.get('referral'):
        ar = AdmissionReferral()
        ar.referral_choice_id = ReferralChoice.objects.get(pk=request.POST.get('referral')).id
        ar.referral_organization = get_object_or_None(Organization, id=request.POST.get('referral_organization'))
        ar.referral_professional = get_object_or_None(CareProfessional, id=request.POST.get('referral_professional'))
        ar.signed_bythe_client = True if request.POST.get('signed') else False
        ar.client = object
        ar.save()

    object.save()

    messages.success(request, _('Admission saved successfully'))

    return HttpResponseRedirect('/client/%s/home' % object.id)

def attach_save(request, object_id = None):
    object = get_object_or_404(Client, pk = object_id, person__organization=request.user.get_profile().org_active)

    # check access by requested user
    if not _access_check(request, object):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    if request.method == 'POST':
        user = request.user
        filename = ''

        if 'file' in request.FILES:
            path = '%simg/organization/%s' % (settings.MEDIA_ROOT, user.get_profile().org_active.id)
            if not os.path.exists(path):
                os.mkdir(path)
                os.chmod(path, 0777)

            path = '%simg/organization/%s/attach' % (settings.MEDIA_ROOT, user.get_profile().org_active.id)
            if not os.path.exists(path):
                os.mkdir(path)
                os.chmod(path, 0777)

            try:
                    filename = request.FILES['file']
                    file = str(uuid.uuid4()) + '.'+ (str(filename).split('.')[-1])
                    destination = open('%s/%s' % (path,  file), 'w+')

                    for chunk in filename.chunks():
                        destination.write(chunk)
                    destination.close()

                    attach = Attach()
                    if not request.POST.get('signed'):
                        attach.signed_bythe_client = False
                    else:
                        attach.signed_bythe_client = True

                    attach.filename = '%s' %  filename
                    attach.description = request.POST.get('description')
                    attach.file = '%s' % file
                    attach.type = request.POST.get('doc_type')
                    attach.client = object
                    attach.save()

            except IOError:
                print "error sending file"

        return HttpResponseRedirect('/admission/%s/' % object_id)
        return HttpResponseRedirect('/admission/%s/' % object_id)
