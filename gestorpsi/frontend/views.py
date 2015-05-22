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

from gestorpsi.settings import ADMIN_URL

def start(request):

    # admin do not have profile
    try:
        profile = request.user.get_profile()
    except:
        return HttpResponseRedirect(ADMIN_URL)

    date = datetime.now()

    #code for testing the charging system
    #from gestorpsi.async_tasks.tasks import check_and_charge
    #check_and_charge()

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
        return render_to_response('frontend/frontend_careprofessional_start.html', locals(), context_instance=RequestContext(request))
    
    """ user's employee home page """
    if request.user.get_profile().person.is_employee():
        """ items to be added in secretary home page:
            - today event list
            - referrals (complete information)
            - queue """
        return HttpResponseRedirect('/schedule/events/')

    raise Http404


