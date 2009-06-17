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

# Eu sou apenas uma linha de testes. Por favor, delete-me! =)

import calendar
import locale
from dateutil import parser
from datetime import datetime, timedelta
from django import http
from django.template.context import RequestContext
from django.shortcuts import get_object_or_404, render_to_response, HttpResponse
from django.utils.translation import gettext as _
from django.utils import simplejson
from swingtime.forms import MultipleOccurrenceForm
from swingtime.utils import create_timeslot_table
from gestorpsi.schedule.models import ScheduleOccurrence
from gestorpsi.referral.models import Referral
from gestorpsi.referral.forms import ReferralForm
from gestorpsi.place.models import Place, Room
from gestorpsi.service.models import Service
from gestorpsi.careprofessional.models import CareProfessional
from gestorpsi.device.models import DeviceDetails
from gestorpsi.schedule.forms import ScheduleOccurrenceForm, ScheduleSingleOccurrenceForm
from gestorpsi.util.decorators import permission_required_with_403

@permission_required_with_403('schedule.schedule_list')
def schedule_occurrence_listing(request, year = 1, month = 1, day = None, 
    template='schedule/schedule_events.html',
    **extra_context):

    occurrences = schedule_occurrences(request, year, month, day)

    
    
    return render_to_response(
        template, 
        dict(extra_context, occurrences=occurrences),
        context_instance=RequestContext(request)
    )


@permission_required_with_403('schedule.schedule_list')
def schedule_occurrence_listing_today(request, template='schedule/schedule_events.html'):
    return schedule_occurrence_listing(request, datetime.now().strftime('%Y'), datetime.now().strftime('%m'), datetime.now().strftime('%d'))

@permission_required_with_403('schedule.schedule_write')
def add_event(
    request, 
    template='schedule/schedule_form.html',
    event_form_class=ReferralForm,
    recurrence_form_class=ScheduleOccurrenceForm
):
    dtstart = None
    if request.method == 'POST':
        recurrence_form = recurrence_form_class(request.POST)
        event = Referral.objects.get(pk=request.POST['referral'])
        if recurrence_form.is_valid():
            recurrence_form.save(event)
            return HttpResponse(event.id)

    else:
        if 'dtstart' in request.GET:
            try:
                dtstart = parser.parse(request.GET['dtstart'])
            except:
                # TODO A badly formatted date is passed to add_event
                dtstart = datetime.now()
        if 'room' in request.GET:
            room = request.GET['room']
        else:
            room = None
        event_form = event_form_class()
        recurrence_form = recurrence_form_class(initial=dict(
            dtstart=dtstart, 
            room=room, 
            day=datetime.strptime(dtstart.strftime("%Y-%m-%d"), "%Y-%m-%d"), 
            until=datetime.strptime(dtstart.strftime("%Y-%m-%d"), "%Y-%m-%d"),
            ))
            
    return render_to_response(
        template,
        dict(dtstart=dtstart, event_form=event_form, recurrence_form=recurrence_form),
        context_instance=RequestContext(request)
    )


@permission_required_with_403('schedule.schedule_read')
def event_view(
    request, 
    pk, 
    template='schedule/event_detail.html', 
    event_form_class=ReferralForm,
    recurrence_form_class=ScheduleOccurrenceForm
):

    event = get_object_or_404(Referral, pk=pk)
    event_form = recurrence_form = None
    if request.method == 'POST':
        if '_update' in request.POST:
            event_form = event_form_class(request.POST, instance=event)
            if event_form.is_valid():
                event_form.save(event)
                return http.HttpResponseRedirect(request.path)
        elif '_add' in request.POST:
            recurrence_form = recurrence_form_class(request.POST)
            if recurrence_form.is_valid():
                recurrence_form.save(event)
                return http.HttpResponseRedirect(request.path)
        else:
            return http.HttpResponseBadRequest('Bad Request')

    event_form = event_form or event_form_class(instance=event)
    if not recurrence_form:
        recurrence_form = recurrence_form_class(
            initial=dict(dtstart=datetime.now())
        )
            
    return render_to_response(
        template, 
        dict(event=event, event_form=event_form, recurrence_form=recurrence_form),
        context_instance=RequestContext(request)
    )

@permission_required_with_403('schedule.schedule_read')
def occurrence_view(
    request, 
    event_pk, 
    pk, 
    template='schedule/schedule_occurrence_form.html',
    form_class=ScheduleSingleOccurrenceForm
):
    user = request.user
    rooms = Room.objects.filter(place__organization = user.profile.org_active)
    occurrence = get_object_or_404(ScheduleOccurrence, pk=pk, event__pk=event_pk)
    if request.method == 'POST':
        form = form_class(request.POST, instance=occurrence)
        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect(request.path)
    else:
        form = form_class(instance=occurrence)
        
    return render_to_response(
        template,
        dict(occurrence=occurrence, form=form, rooms=rooms),
        context_instance=RequestContext(request)
    )

@permission_required_with_403('schedule.schedule_list')
def _datetime_view(
    request, 
    template, 
    dt, 
    timeslot_factory=None, 
    items=None,
    params=None
):

    user = request.user
    timeslot_factory = timeslot_factory or create_timeslot_table
    params = params or {}
    data = dict(
        day=dt, 
        next_day=dt + timedelta(days=+1),
        prev_day=dt + timedelta(days=-1),
        timeslots=timeslot_factory(dt, items, **params),
        places = Place.objects.filter(organization=request.user.get_profile().org_active.id),
        services = Service.objects.filter(organization=request.user.get_profile().org_active.id),
        professionals = CareProfessional.objects.filter(person__organization=request.user.get_profile().org_active.id),
        devices = DeviceDetails.objects.all(),
        event_form = ReferralForm(),
        recurrence_form = ScheduleOccurrenceForm(),
        rooms = Room.objects.filter(place__organization = user.profile.org_active)
    )

    return render_to_response(
        template,
        data,
        context_instance=RequestContext(request)
    )

@permission_required_with_403('schedule.schedule_list')
def schedule_index(request, 
    year = datetime.now().strftime("%Y"), 
    month = datetime.now().strftime("%m"), 
    day = datetime.now().strftime("%d"), 
    template='schedule/schedule_index.html',
     **params):
    
    # Test if clinic administrator has registered referrals before access schedule page.
    if not Referral.objects.filter(status='01', organization=request.user.get_profile().org_active).count():
        return render_to_response('schedule/schedule_referral_alert.html', {'object': _("There's no Referral created yet. Please, create one before access Schedule."), }, context_instance=RequestContext(request))    

    return _datetime_view(request, template, datetime(int(year), int(month), int(day)), **params)

@permission_required_with_403('schedule.schedule_list')
def today_occurrences(request):
    return daily_occurrences(request, datetime.now().strftime("%Y"), datetime.now().strftime("%m"), datetime.now().strftime("%d"))

@permission_required_with_403('schedule.schedule_list')
def schedule_occurrences(request, year = 1, month = 1, day = None):
    if day:
        date_start = datetime.strptime("%s%s%s" % (year, month, day),"%Y%m%d")
        date_end = date_start+timedelta(days=+1)
    else:
        date_start = datetime.strptime("%s%s" % (year, month),"%Y%m")
        date_end = date_start+timedelta( days=calendar.monthrange(int(year), int(month))[1] + 0)

    return ScheduleOccurrence.objects.filter(
        start_time__gte=date_start,
        start_time__lt=date_end,
        event__referral__organization=request.user.get_profile().org_active.id,
    )

@permission_required_with_403('schedule.schedule_list')
def daily_occurrences(request, year = 1, month = 1, day = None):
    #locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    #locale.setlocale(locale.LC_ALL,'en_US.UTF-8')
    locale.setlocale(locale.LC_ALL,'pt_BR.ISO8859-1')
    occurrences = schedule_occurrences(request, year, month, day)

    array = {} #json
    i = 0
    
    date = datetime.strptime(('%s/%s/%s' % (year, month, day)), "%Y/%m/%d")

    array['util'] = {
        'date': ('%s-%s-%s' % (year, month, day)),
        'date_field': ('%s/%s/%s' % (year, month, day)),
        'str_date': '%s, %s %s %s %s %s' % (date.strftime("%A"), date.strftime("%d"), _('of'), date.strftime("%B"), _('of'), date.strftime("%Y")),
        'next_day': (date + timedelta(days=+1)).strftime("%Y/%m/%d"),
        'prev_day': (date + timedelta(days=-1)).strftime("%Y/%m/%d"),
        'weekday': date.weekday(),
    }
    
    for o in occurrences:
        range = o.end_time-o.start_time
        rowspan = range.seconds/1800 # how many blocks of 30min the occurrence have
        
        array[i] = {
            'id': o.id,
            'event_id': o.event.id,
            'room': o.room_id,
            'place': o.room.place_id,
            'room_name': ("%s" % o.room),
            'service_id':o.event.referral.service.id,
            'service':o.event.referral.service.name,
            'css_color_class':o.event.referral.service.css_color_class,
            'start_time': o.start_time.strftime('%H:%M:%S'),
            'end_time': o.end_time.strftime('%H:%M:%S'),
            'rowspan': rowspan,
        }
        
        sub_count = 0
        array[i]['professional'] = {}
        for p in o.event.referral.professional.all():
            array[i]['professional'][sub_count] = ({'id':p.id, 'name':p.person.name})
            sub_count = sub_count + 1
        
        sub_count = 0
        array[i]['client'] = {}
        for c in o.event.referral.client.all():
            array[i]['client'][sub_count] = ({'id':c.id, 'name':c.person.name})
            sub_count = sub_count + 1

        i = i + 1

    array['util']['occurrences_total'] = i
    array = simplejson.dumps(array, encoding = 'iso8859-1')
    
    return HttpResponse(array, mimetype='application/json')
    

@permission_required_with_403('schedule.schedule_read')
def occurrence_abstract(request, object_id = None):
    try:
        o = ScheduleOccurrence.objects.get(pk=object_id)
    except:
        raise http.Http404

    array = {} #json

    array['id'] = o.id
    array['event_id'] = o.event.id
    array['date'] = o.start_time.strftime('%d/%m/%Y %H:%M')
    array['day'] = o.start_time.strftime('%Y/%m/%d')
    array['room'] = o.room.description
    array['service'] = o.event.referral.service.name
    
    array['professional'] = {}
    count = 0
    for p in o.event.referral.professional.all():
        array['professional'][count] = ({
            'id':p.id, 
            'name':p.person.name,
            'phone':p.person.get_phones(),
            })
        count = count + 1

    count = 0
    array['client'] = {}
    for c in o.event.referral.client.all():
        array['client'][count] = ({
            'id':c.id, 
            'name':c.person.name,
            'phone':c.person.get_phones(),
            })
        count = count + 1

    array = simplejson.dumps(array, encoding = 'iso8859-1')
    
    return HttpResponse(array, mimetype='application/json')

@permission_required_with_403('schedule.schedule_read')
def referral_occurrences(request, object_id = None):
    try:
        o = Referral.objects.get(pk=object_id)
    except:
        raise http.Http404

    array = {} #json

    array['id'] = o.id;
    array['service'] = o.service.name;
    array['annotation'] = o.annotation;
    
    array['professional'] = {}
    count = 0
    for p in o.professional.all():
        array['professional'][count] = ({
            'id':p.id, 
            'name':p.person.name,
            'phone':p.person.get_phones(),
            })
        count = count + 1

    count = 0
    array['client'] = {}
    for c in o.client.all():
        array['client'][count] = ({
            'id':c.id, 
            'name':c.person.name,
            'phone':c.person.get_phones(),
            })
        count = count + 1
    
    count = 0
    array['occurrences'] = {}
    for i in o.occurrence_set.all():
        array['occurrences'][count] = ({
            'id':i.id,
            'date':i.start_time.strftime('%d/%m/%Y'),
            'start_time':i.start_time.strftime('%H:%M'),
            'end_time':i.end_time.strftime('%H:%M'),
            'room':i.scheduleoccurrence.room.description,
            'place':i.scheduleoccurrence.room.place.label,
            })
        count = count + 1

    array = simplejson.dumps(array)
    
    return HttpResponse(array, mimetype='application/json')
