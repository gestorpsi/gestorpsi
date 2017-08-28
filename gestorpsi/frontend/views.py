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
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext as _

from gestorpsi.client.models import Client
from gestorpsi.careprofessional.models import CareProfessional
from gestorpsi.schedule.views import schedule_occurrences
from gestorpsi.referral.models import Queue
from gestorpsi.person.models import Person
from gestorpsi.settings import ADMIN_URL

from gestorpsi.frontend.models import FrontendProfile
from gestorpsi.frontend.forms import FrontendProfileForm

def birthdate_filter(request, frm=None, month=None, object=None, active=True, sort='increase'):
    """
        Birth date filter:

        return array of Person object

        frm : string
                secretary: 
                    all person of organization
                careprofessional
                    clients of professional

        month  : integer / month of year
        object : Careprofessional object
        active : boolean : filter active or inactive Client
        sort   : string: decreasing or indecrasing
    """
    # birthDate of month, order by day
    birthdate_list = [] # person object

    # increasing
    sort_list = range(1,32)
    # decreasing
    if sort == 'decreasing':
        sort_list.reverse()

    if frm == 'secretary':
        for d in sort_list:
            for p in Person.objects.filter(client__active=active,\
                    birthDate__month=month,\
                    birthDate__day=d,\
                    organization=request.user.get_profile().org_active).order_by('name'):
                if not p in birthdate_list:
                    birthdate_list.append(p)
    
    # filter by careprofessional (object)
    if frm == 'careprofessional':
        for d in sort_list:
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

    # no frontendProfile
    if not FrontendProfile.objects.filter(user=request.user):
        return HttpResponseRedirect('/frontend/settings/')

    date = datetime.now()

    # list
    list_subscribe = False
    list_queue = False
    list_birthdate = False
    list_schedule = False
    list_student = False
    list_client = False
    list_service = False
    list_referral = False

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

        list_schedule = schedule_occurrences(request, datetime.now().strftime('%Y'), datetime.now().strftime('%m'), datetime.now().strftime('%d')).filter(event__referral__professional=object)
        if request.user.frontendprofile.referral > 0:
            if request.user.frontendprofile.referral_sort == 1:
                list_referral = object.referral_set.filter(status='01').order_by('-date')[:request.user.frontendprofile.referral]
            else:
                list_referral = object.referral_set.filter(status='01').order_by('date')[:request.user.frontendprofile.referral]

        if request.user.frontendprofile.queue > 0:
            if request.user.frontendprofile.queue_sort == 1:
                list_queue = Queue.objects.filter(referral__professional=object, date_out=None).order_by('-date_in')
            else:
                list_queue = Queue.objects.filter(referral__professional=object, date_out=None).order_by('date_in')

        if request.user.frontendprofile.birthdate_client > 0:
            if request.user.frontendprofile.birthdate_client_sort == 1:
                list_birthdate = birthdate_filter(request, 'careprofessional', month, object, active, 'increase')
            else:
                list_birthdate = birthdate_filter(request, 'careprofessional', month, object, active, 'decrease')

        return render_to_response('frontend/frontend_careprofessional_start.html', locals(), context_instance=RequestContext(request))
    
    """ user's employee home page """
    if request.user.get_profile().person.is_employee():
        """
            events of all careprofessional
            birth date of all persons
        """
        birthdate_list = birthdate_filter(request, 'secretary', month, active)
        events = schedule_occurrences(request,\
                datetime.now().strftime('%Y'),\
                datetime.now().strftime('%m'),\
                datetime.now().strftime('%d')).filter(event__referral__professional__person__organization=request.user.get_profile().org_active )
        return render_to_response('frontend/frontend_secretary.html', locals(), context_instance=RequestContext(request))

    raise Http404


def settings(request):
    """
        save custom itens to show in FrontEnd home of User
    """
    if request.POST:
        """
            save OR update profile
            redirect to render form
        """
        if FrontendProfile.objects.filter(user=request.user):
            form = FrontendProfileForm(request.POST, instance=request.user.frontendprofile)
        else:
            prof = FrontendProfile()
            prof.user = request.user
            prof.save()
            form = FrontendProfileForm(request.POST, instance=prof)

        if form.is_valid():
            form_save = form.save()
            messages.success(request, _(u'Configuração salva com sucesso!'))
            return HttpResponseRedirect('/frontend/settings/')
        else:
            messages.error(request, _(u'Valor invalido!'))

    else:
        """
            get OR create a profile
            render form
        """
        if FrontendProfile.objects.filter(user=request.user):
            form = FrontendProfileForm(instance=request.user.frontendprofile)
        else:
            form = FrontendProfileForm()

    tab_settings_class = 'active'  # tab settings active
    return render_to_response('frontend/frontend_settings.html', locals(), context_instance=RequestContext(request))
