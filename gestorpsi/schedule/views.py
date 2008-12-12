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
from gestorpsi.place.models import Place, Room
from gestorpsi.careprofessional.models import CareProfessional
from gestorpsi.service.models import Service
from gestorpsi.client.models import Client
from gestorpsi.person.views import person_order
from gestorpsi.referral.models import Referral

def index(request):
    user = request.user
    calendar.setfirstweekday(6)
    today = datetime.datetime.now().strftime('%Y-%m-%d')
#    cal = calendar.HTMLCalendar(calendar.SUNDAY)
#    month = calendar.monthcalendar(today.year, today.month)
# print month[1]
    places = Place.objects.filter(organization=user.org_active.id)
    professionals = CareProfessional.objects.filter(person__organization = user.org_active.id)
    services = Service.objects.filter( active=True, organization=user.org_active )
    clients = person_order(Client.objects.filter(person__organization = user.org_active.id, clientStatus = '1'))
    week_header = schedule_week_header()
    return render_to_response('schedule/schedule_index.html', locals())

def save(request):
    client = request.POST['client']
    time_date = request.POST['time_date']
    hour = request.POST['hour']
    duration = request.POST['duration']
    repeat = request.POST['repeat']
    professional = request.POST['professional']
    service = request.POST['service']
    room = request.POST['room']
    comments = request.POST['comments']

    print u"%s" % client
    print u"%s" % time_date
    print u"%s" % hour
    print u"%s" % duration
    print u"%s" % repeat
    if repeat == '7':
        lista_semana = request.POST.getlist('weekly')
        for w in lista_semana:
            print w
    print u"%s" % professional
    print u"%s" % service
    print u"%s" % room
    print u"%s" % comments

    return HttpResponse('walaaa')

#    try:
#        referral = Referral.objects.get(pk=request.POST['referral'])
#    except:
#        referral()
#    room = Room.objects.get(pk=request.POST['room'])
#    app_date = request.POST['initial appointment date']
#    initial_hour = request.POST['get begin time']
#    final_hour = request.POST['get finish time']
#    repeat = request.POST['how long will last (in weeks)']
#    for i in range(0, repeat):
#        schedule = Schedule()
#        schedule.referral = referral
#        schedule.room = room
#        schedule.appointment_begin = app_date + initial_hour
#        schedule.appointment_end = app_date + final_hour
#        schedule.save()
#        app_date = app_date + 7 # days
#    return HttpResponse('foo bar')=======

def schedule_week_header(today=datetime.datetime.now()):
	calendar.setfirstweekday(6)
	month = calendar.monthcalendar(today.year, today.month)
	week_header = []
	for w in month:
		if today.day in w:
			for d in w:
				week_header.append(datetime.date(today.year, today.month, d))
	return week_header