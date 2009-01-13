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

import datetime
import calendar
import time
from datetime import datetime as datetime2
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from gestorpsi.place.models import Place, Room
from gestorpsi.careprofessional.models import CareProfessional
from gestorpsi.service.models import Service
from gestorpsi.client.models import Client
from gestorpsi.person.views import person_order
from gestorpsi.referral.models import Referral
from gestorpsi.schedule.models import Schedule
#from django.core import serializers
from django.utils import simplejson

def schedules_in_range(request, date_start = datetime.datetime.now().strftime('%Y%m%d%H%M%S'), date_end = datetime.datetime.now().strftime('%Y%m%d%H%M%S')):
	date_start = datetime2.strptime(date_start, "%Y%m%d%H%M%S")
	date_end = datetime2.strptime(date_end, "%Y%m%d%H%M%S")

	schedules = Schedule.objects.filter(Q(appointment_begin__gt=date_start) & Q(appointment_end__lt=date_end))
	array = {}
	i = 0
	for s in schedules:
		array[i] = {
			'schedule': s.id,
			'professional_id':s.referral.professional_id,
			'professional':s.referral.professional.person.name,
			'service_id':s.referral.service_id,
			'service':s.referral.service.description,
			'client_id':s.referral.client_id,
			'client':s.referral.client.person.name,
			'room_id':s.room_id,
			'room':s.room.description,
			'date_start': s.appointment_begin.strftime('%Y%m%d'),
			'time_start': s.appointment_begin.strftime('%H%M%S'),
			'date_start': s.appointment_end.strftime('%Y%m%d'),
			'date_end': s.appointment_end.strftime('%H%M%S'),
			}
		i = i + 1

	array = simplejson.dumps(array)
	return HttpResponse(array, mimetype='application/json')

def schedules_daily(request, date_start = datetime.datetime.now().strftime('%Y%m%d')):
	return schedules_in_range(request, '%s%s' % (date_start, '000000'), '%s%s' % (date_start, '235959'))

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
    client = Client.objects.get(pk=request.POST['client'])
    professional = CareProfessional.objects.get(pk=request.POST['professional'])
    service = Service.objects.get(pk=request.POST['service'])
    try:
        room = Room.objects.get(pk=request.POST['room'])
    except:
        room = Room.objects.all()[0]
    duration = datetime.timedelta(minutes=int(request.POST['duration']))

    schedule = Schedule()
    schedule.referral =  Referral.objects.create(client=client, professional=professional, service=service)
    schedule.room = room
    schedule.appointment_begin = datetime.datetime(*time.strptime((request.POST['time_date'] + " " + request.POST['hour']), "%d/%m/%Y %H:%M")[:6])
    schedule.appointment_end = schedule.appointment_begin + duration
    schedule.save()

    return HttpResponse(schedule.id)

def save_tests(request):
    client = request.POST['client']
    time_date = request.POST['time_date']
    repeat_date = request.POST['repeat_date']
    hour = request.POST['hour']
    duration = request.POST['duration']
    repeat = request.POST['repeat']
    professional = request.POST['professional']
    service = request.POST['service']
    room = request.POST['room']
    comments = request.POST['comments']

    date_begin = datetime.datetime(*time.strptime((time_date + " " + hour), "%d/%m/%Y %H:%M")[:6])
    date_end = datetime.datetime(*time.strptime((repeat_date + " " + hour), "%d/%m/%Y %H:%M")[:6])
    duracao = datetime.timedelta(minutes=int(duration))

    app_ini = date_begin #datetime.datetime(*time.strptime((time_date + " " + hour), "%d/%m/%Y %H:%M")[:6])
    app_end = app_ini + duracao

    if repeat == '1':
        print "agendamento diario"

    if repeat == '7':
        week, days = divmod(time_date - repeat_date)
        app_ini = app_ini + datetime.timedelta(weeks=1)
        app_end = app_ini + duracao

    if repeat == '30':
        print "agendamento mensal"


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