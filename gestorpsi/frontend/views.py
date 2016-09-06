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
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from gestorpsi.client.models import Client
from gestorpsi.careprofessional.models import CareProfessional
from gestorpsi.schedule.views import schedule_occurrences
from gestorpsi.referral.models import Queue
from gestorpsi.person.models import Person
from gestorpsi.settings import ADMIN_URL

def birthdate_filter(request, frm=None, month=None, object=None, active=True):
    """
        Birth date filter:

        return array of Person object

        frm : string
                secretary: 
                    all person of organization
                careprofessional
                    clients of professional

        month : integer / month of year
        object : Careprofessional object
        active : boolean : filter active or inactive Client
    """
    # birthDate of month, order by day
    birthdate_list = [] # person object

    if frm == 'secretary':
        for d in range(1,32):
            for p in Person.objects.filter(client__active=active,\
                    birthDate__month=month,\
                    birthDate__day=d,\
                    organization=request.user.get_profile().org_active).order_by('name'):
                if not p in birthdate_list:
                    birthdate_list.append(p)
    
    # filter by careprofessional (object)
    if frm == 'careprofessional':
        for d in range(1,32):
            for p in Client.objects.filter(referral__professional=object,\
                    active=active,\
                    person__organization=request.user.get_profile().org_active,\
                    person__birthDate__month=month,\
                    person__birthDate__day=d).order_by('person__name'):
                if not p in birthdate_list:
                    birthdate_list.append(p.person)

    return birthdate_list


def start(request):

    # admin do not have profile
    try:
        profile = request.user.get_profile()
    except:
        return HttpResponseRedirect(ADMIN_URL)

    date = datetime.now()

    # current month
    month = (datetime.now().month) # integer
    month_string = datetime.now().strftime("%B").capitalize # string
    month_list = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']
    active = True

    if request.POST:
        month = int(request.POST.get('month_filter')) # integer
        month_string  = month_list[int(month)-1]
        active_filter = int(request.POST.get('active_filter')) # integer
        active = True if active_filter == 1 else False

    """ user's client home page """
    if request.user.get_profile().person.is_client():
        object = Client.objects.get(pk=request.user.get_profile().person.client.id)
        return render_to_response('frontend/frontend_client_start.html', locals(), context_instance=RequestContext(request))
    
    """ user's professional and student home page """
    if request.user.get_profile().person.is_careprofessional() or request.user.get_profile().person.is_student():
        object = CareProfessional.objects.get(pk=request.user.get_profile().person.careprofessional.id)
        events = schedule_occurrences(request, datetime.now().strftime('%Y'), datetime.now().strftime('%m'), datetime.now().strftime('%d')).filter(event__referral__professional=object)
        referrals = object.referral_set.filter(status='01').order_by('-date')[:10]
        queues = Queue.objects.filter(referral__professional=object, date_out=None).order_by('priority','date_in')
        birthdate_list = birthdate_filter(request,'careprofessional',month,object,active)
        return render_to_response('frontend/frontend_careprofessional_start.html', locals(), context_instance=RequestContext(request))
    
    """ user's employee home page """
    if request.user.get_profile().person.is_employee():
        """
            events of all careprofessional
            birth date of all persons
        """
        birthdate_list = birthdate_filter(request,'secretary',month,active)
        events = schedule_occurrences(request,\
                datetime.now().strftime('%Y'),\
                datetime.now().strftime('%m'),\
                datetime.now().strftime('%d')).filter(event__referral__professional__person__organization=request.user.get_profile().org_active )
        return render_to_response('frontend/frontend_secretary.html', locals(), context_instance=RequestContext(request))

    raise Http404
