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

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
import datetime, calendar
from gestorpsi.place.models import Place
from gestorpsi.careprofessional.models import CareProfessional
from gestorpsi.service.models import Service
from gestorpsi.client.models import Client
from gestorpsi.person.views import person_order

def index(request):
    user = request.user
#    today = datetime.datetime.now()
#    cal = calendar.HTMLCalendar(calendar.SUNDAY)
#    month = calendar.monthcalendar(today.year, today.month)
    places = Place.objects.filter(organization=user.org_active.id)
    professionals = CareProfessional.objects.filter(person__organization = user.org_active.id)
    services = Service.objects.filter( active=True, organization=user.org_active )
    clients = person_order(Client.objects.filter(person__organization = user.org_active.id, clientStatus = '1'))

    return render_to_response('schedule/schedule_index.html', locals())
