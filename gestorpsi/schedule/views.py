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

import calendar
from dateutil import parser
from datetime import datetime, timedelta
import datetime as datetime_
from django import http
from django.forms.util import ErrorList
from django.template.context import RequestContext
from django.shortcuts import get_object_or_404, render_to_response, HttpResponse
from django.utils.translation import ugettext as _
from django.utils import simplejson
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from swingtime.utils import create_timeslot_table
from gestorpsi.schedule.models import ScheduleOccurrence, OccurrenceConfirmation, OccurrenceFamily, OccurrenceEmployees, Occurrence
from gestorpsi.referral.models import Referral
from gestorpsi.referral.forms import ReferralForm
from gestorpsi.place.models import Place, Room
from gestorpsi.service.models import Service, ServiceGroup
from gestorpsi.careprofessional.models import CareProfessional
from gestorpsi.client.models import Client
from gestorpsi.schedule.forms import ScheduleOccurrenceForm, ScheduleSingleOccurrenceForm
from gestorpsi.util.decorators import permission_required_with_403
from gestorpsi.util.views import get_object_or_None
from gestorpsi.schedule.forms import OccurrenceConfirmationForm
from gestorpsi.device.models import DeviceDetails
from gestorpsi.organization.models import TIME_SLOT_SCHEDULE
from gestorpsi.authentication.models import Profile
from gestorpsi.person.models import Person


def _access_check_by_occurrence(request, occurrence):
    #from gestorpsi.client.views import _access_check_referral_write, _access_check
    from gestorpsi.client.views import _access_check
    denied_to_read = None
    for c in occurrence.event.referral.client.all():
        if not _access_check(request, c):
            denied_to_read = True

    if denied_to_read:
        return False

    return True

# restrict information of schedules booked for professional and student profiles
def hide_schedule_information(user):
    profile = Profile.objects.get(person=user.get_profile().person_id, person__organization=user.get_profile().org_active)
    restrict = user.get_profile().org_active.restrict_schedule

    for g in profile.user.groups.all():
        if g.name == "administrator" or not restrict:
            restrict = False
            break
        if g.name == "professional" or g.name == "student":
            restrict = True

    return restrict

@permission_required_with_403('schedule.schedule_list')
def schedule_occurrence_listing(request, place_id, year = 1, month = 1, day = None,
    template='schedule/schedule_events.html',
    **extra_context):

    occurrences = schedule_occurrences(request, year, month, day)

    try:
        place = Place.objects.get( pk=place_id )
    except:
        place = Place.objects.filter(place_type=1, organization=request.user.get_profile().org_active)[0]

    return render_to_response(
        template,
        dict(
            extra_context,
            occurrences=occurrences,
            path = "events/",
            places_list = Place.objects.active().filter(organization=request.user.get_profile().org_active.id),
            place = place,
            services = Service.objects.active().filter(organization=request.user.get_profile().org_active.id),
            professionals = CareProfessional.objects.active(request.user.get_profile().org_active.id),
            tab_event_class = 'active',
            ),
        context_instance=RequestContext(request)
    )


@permission_required_with_403('schedule.schedule_list')
def schedule_occurrence_listing_today(request, place=None, template='schedule/schedule_events.html'):
    return schedule_occurrence_listing(request, place, datetime.now().strftime('%Y'), datetime.now().strftime('%m'), datetime.now().strftime('%d'))

def invalid_delta_time(start, end):
    return start >= end

def verify_client(referral):
    return referral is not None

@permission_required_with_403('schedule.schedule_write')
def add_event(
        request, 
        template='schedule/schedule_form.html',
        event_form_class=ReferralForm,
        recurrence_form_class=ScheduleOccurrenceForm,
        redirect_to = None
    ):

    # have to contains dtstart variable in URL. URL from schedule have to contains date and time informations.
    if not 'dtstart' in request.GET:
        return http.HttpResponseRedirect('/schedule/')

    if request.method == 'POST':
        if int(request.POST.get('count')) > 40: # limit occurrence repeat
            return render_to_response('403.html', {'object':_('Sorry. You can not book more than 40 occurrence at the same time')})
        recurrence_form = recurrence_form_class(request.POST)

        if recurrence_form.is_valid():
            if invalid_delta_time(request.POST.get('start_time_delta'), request.POST.get('end_time_delta')):
                messages.error(request, _('The start time should be less than the end time'))
                return http.HttpResponseRedirect(request.META.get('HTTP_REFERER') or '/schedule/')


            devices = DeviceDetails.objects.filter(id__in=request.POST.getlist('device')) # filter devices based on selection
            start_occurrence_date = end_occurrence_date = datetime(
                year=int(request.POST.get('until_year')),
                month=int(request.POST.get('until_month')),
                day=int(request.POST.get('until_day'))
                )
            start_delta = timedelta(seconds=int(request.POST.get('start_time_delta'))) # create a start delta time
            end_delta = timedelta(seconds=(int(request.POST.get('end_time_delta')) - 1)) # checking till one minute before next session
            start_device_schedule = (start_occurrence_date + start_delta) # get correct start time of device schedule

            end_device_schedule = (end_occurrence_date + end_delta)
            occurrence_start = Occurrence.objects.filter(
                start_time__range=(
                    start_device_schedule,
                    end_device_schedule),
                scheduleoccurrence__device__in=devices,
                ) # try to check if there's any occurrence with the device in specified time
            end_delta= timedelta(seconds=int(request.POST.get('end_time_delta'))) # check exact end time
            end_device_schedule = (end_occurrence_date + end_delta)
            occurrence_end = Occurrence.objects.filter(
                end_time__range=(
                    start_device_schedule,
                    end_device_schedule),
                scheduleoccurrence__device__in=devices,
                )
            if len(occurrence_start) is not 0 or len(occurrence_end) is not 0:
                error = recurrence_form._errors.setdefault('device', ErrorList())
                error.append('Selected device is busy')


            if request.POST.get('tabtitle'): # booking single client
                if verify_client(request.POST.get('referral')) == False:
                    messages.error(request, _('Check the mandatory fields'))
                    return http.HttpResponseRedirect(request.META.get('HTTP_REFERER') or '/schedule/')
                referral = get_object_or_404(Referral, pk=request.POST.get('referral'), service__organization=request.user.get_profile().org_active)
                event = recurrence_form.save(referral)
            elif request.POST.get('group'): # booking a group
                group = get_object_or_404(ServiceGroup, pk=request.POST.get('group'), service__organization=request.user.get_profile().org_active, active=True)
                if group.charged_members(): # this check is already done in template. just to prevent empty groups
                    first = True
                    for group_member in group.charged_members():
                        if first:
                            event = recurrence_form.save(group_member.referral)
                            first = False
                        else:
                            if not event.errors:
                                event = recurrence_form.save(group_member.referral, True) # ignore busy check
            else:
                referral = get_object_or_404(Referral, pk=request.POST.get('select_referral'), service__organization=request.user.get_profile().org_active)
                event = recurrence_form.save(referral, True, True)
                    
            if not event.errors:
                messages.success(request, _('Schedule saved successfully'))
                return http.HttpResponseRedirect(redirect_to or '/schedule/')
            else:
                return render_to_response(
                    'schedule/event_detail.html',
                    dict(event=event),
                    context_instance=RequestContext(request)
                )
    else:

        dtstart = parser.parse( request.GET['dtstart'] )
        room = get_object_or_None(Room, pk=request.GET.get('room'), place__organization=request.user.get_profile().org_active)
        client = get_object_or_None(Client, pk = request.GET.get('client'), person__organization=request.user.get_profile().org_active)
        referral = get_object_or_None(Referral, pk = request.GET.get('referral'), service__organization=request.user.get_profile().org_active)
        event_form = event_form_class()

        recurrence_form = recurrence_form_class(initial=dict(
                dtstart=dtstart, 
                day=datetime.strptime(dtstart.strftime("%Y-%m-%d"), "%Y-%m-%d"), 
                until=datetime.strptime(dtstart.strftime("%Y-%m-%d"), "%Y-%m-%d"),
                room=room.id,
            ))

        recurrence_form.fields['device'].widget.choices = [(i.id, i) for i in DeviceDetails.objects.active(request.user.get_profile().org_active).filter(Q(room=room) | Q(mobility="2", lendable=True) | Q(place=room.place, mobility="2", lendable=False))]

    return render_to_response(
        template,
        dict(
            dtstart=dtstart,
            event_form=event_form,
            recurrence_form=recurrence_form,
            group  = ServiceGroup.objects.filter(service__organization = request.user.get_profile().org_active, active=True),
            room = room,
            object = client,
            referral = referral,
            referrals = Referral.objects.all(),
            room_id=room.id,
            ),
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

    event = get_object_or_404(Referral, pk=pk, service__organization=request.user.get_profile().org_active)
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

    occurrence = get_object_or_404(ScheduleOccurrence, pk=pk, event__pk=event_pk, event__referral__service__organization=request.user.get_profile().org_active)
    if request.method == 'POST':

        form = form_class(request.POST, instance=occurrence)
        if form.is_valid():
            form.save()
            messages.success(request, _('Occurrence updated successfully'))
            return http.HttpResponseRedirect(request.path)
        else:
            print form.errors
    else:
        form = form_class(instance=occurrence, initial={'start_time':occurrence.start_time})
        form.fields['device'].queryset = DeviceDetails.objects.filter(Q(room = occurrence.room, mobility="1") | Q(place =  occurrence.room.place, room__place__organization = request.user.get_profile().org_active, mobility="2", lendable=False) | Q(room__place__organization = request.user.get_profile().org_active, mobility="2", lendable=True))
    return render_to_response(
        template,
        dict(occurrence=occurrence, form=form),
        context_instance=RequestContext(request)
    )


@permission_required_with_403('schedule.schedule_write')
def occurrence_confirmation_form(
        request, 
        pk, 
        template='schedule/schedule_occurrence_confirmation_form.html',
        form_class=OccurrenceConfirmationForm,
        client_id = None,
        redirect_to = None,
    ):

    occurrence = get_object_or_404(ScheduleOccurrence, pk=pk, event__referral__service__organization=request.user.get_profile().org_active)

    if not occurrence.scheduleoccurrence.was_confirmed():
        initial_device = [device.pk for device in occurrence.device.all()]
    else:
        initial_device = [device.pk for device in occurrence.occurrenceconfirmation.device.all()]

    # check if requested user have perms to read it
    if not _access_check_by_occurrence(request, occurrence):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    try:
        occurrence_confirmation = OccurrenceConfirmation.objects.get(pk = occurrence.occurrenceconfirmation.id)
    except:
        occurrence_confirmation = None

    object = get_object_or_None(Client, pk = client_id, person__organization=request.user.get_profile().org_active)

    from gestorpsi.client.views import  _access_check_referral_write
    denied_to_write = None

    if not _access_check_referral_write(request, occurrence.event.referral):
        denied_to_write = True

    if request.method == 'POST':
        if denied_to_write:
            return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))
        form = form_class(request.POST, instance = occurrence_confirmation, initial={ 'device':initial_device, })
        if form.is_valid():
            data = form.save(commit=False)
            data.occurrence = occurrence
            if int(data.presence) not in (1,2): # client not arrive, dont save datetime field
                data.date_started = None
                data.date_finished = None
            data.save()
            form.save_m2m()

            # save occurrence comment
            occurrence.annotation = request.POST['occurrence_annotation']
            occurrence.save()
            messages.success(request, _('Occurrence confirmation updated successfully'))
            return http.HttpResponseRedirect(redirect_to or request.path)
        else:
            form.fields['device'].widget.choices = [(i.id, i) for i in DeviceDetails.objects.active(request.user.get_profile().org_active).filter(Q(room=occurrence.room) | Q(mobility=2, lendable=True) | Q(place =  occurrence.room.place, mobility=2, lendable=False))]
            return render_to_response(
                template,
                dict(occurrence=occurrence, form=form, object = object, referral = occurrence.event.referral),
                context_instance=RequestContext(request)
            )
    else:
        if hasattr(occurrence_confirmation, 'presence') and int(occurrence_confirmation.presence) not in (1,2): # load initial data if client dont arrive
            occurrence_confirmation.date_started = occurrence.start_time
            occurrence_confirmation.date_finished = occurrence.end_time

        form = form_class(instance=occurrence_confirmation, initial={
            'occurrence':occurrence,
            'start_time':occurrence.start_time,
            'end_time':occurrence.end_time,
            'device': initial_device,
            })

        form.fields['device'].widget.choices = [(i.id, i) for i in DeviceDetails.objects.active(request.user.get_profile().org_active).filter(Q(room=occurrence.room) | Q(mobility="2", lendable=True) | Q(place=occurrence.room.place, mobility="2", lendable=False))]

    return render_to_response(
        template,
        dict(occurrence=occurrence, form=form, object = object, referral = occurrence.event.referral, occurrence_confirmation = occurrence_confirmation, hide_date_field = True if occurrence_confirmation and int(occurrence_confirmation.presence) > 2 else None, denied_to_write = denied_to_write ),
        context_instance=RequestContext(request)
    )

@permission_required_with_403('schedule.schedule_read')
def occurrence_group(
    request,
    group_id,
    occurrence_id,
    template='schedule/schedule_occurrence_group.html',
    #form_class=OccurrenceConfirmationForm,
):

    group = get_object_or_404(ServiceGroup, pk=group_id, service__organization = request.user.get_profile().org_active, active=True)
    occurrence = get_object_or_404(ScheduleOccurrence, pk=occurrence_id, event__referral__service__organization=request.user.get_profile().org_active)
    group_occurrences = ScheduleOccurrence.objects.filter(start_time=occurrence.start_time, end_time=occurrence.end_time, room=occurrence.room
            ).exclude(occurrenceconfirmation__presence = 4 # unmarked's
            ).exclude(occurrenceconfirmation__presence = 5 # remarked
            ).order_by('occurrenceconfirmation', 'event__referral__client')
    event = occurrence.event.referral

    return render_to_response(
        template,
        locals(),
        #dict(occurrence=occurrence, form=form, object = object, referral = occurrence.event.referral, occurrence_confirmation = occurrence_confirmation, hide_date_field = True if occurrence_confirmation and int(occurrence_confirmation.presence) > 2 else None ),
        context_instance=RequestContext(request)
    )

@permission_required_with_403('schedule.schedule_list')
def _datetime_view(
        request,
        template,
        dt,
        place,
        referral=None,
        client=None,
        timeslot_factory=None,
        items=None,
        params=None
    ):

    '''
        Tiago de Souza Moraes
        place: Place.id
    '''

    try:
        referral = Referral.objects.get(pk=referral, service__organization=request.user.get_profile().org_active)
    except:
        referral = None

    try:
        object = Client.objects.get(pk=client, person__organization=request.user.get_profile().org_active)
    except:
        object = ''

    place = Place.objects.get( pk=place )
    occurrences =  ScheduleOccurrence.objects.filter(start_time__year = dt.year, start_time__month = dt.month, start_time__day = dt.day)

    user = request.user
    timeslot_factory = timeslot_factory or create_timeslot_table
    params = params or {}

    data = dict(
        day=dt,
        next_day=dt + timedelta(days=+1),
        prev_day=dt + timedelta(days=-1),

        # get start_time and end_time_delta from place
        # get schedule slot time from organization
        timeslots=timeslot_factory(dt, items, start_time=datetime_.time( place.hours_work()[0], place.hours_work()[1]),\
                    end_time_delta=timedelta(hours=place.hours_work()[2] ),\
                    time_delta=timedelta( minutes=int(request.user.get_profile().org_active.time_slot_schedule) ),\
                    **params),

        places_list = Place.objects.active().filter(organization=request.user.get_profile().org_active.id),
        place = place,
        place_id = place.id,

        occurrences = occurrences,

        services = Service.objects.active().filter(organization=request.user.get_profile().org_active.id),
        professionals = CareProfessional.objects.active_all(request.user.get_profile().org_active.id),
        referral = referral,
        object = object,
        tab_daily_class = "active", # class object, tab menu
        restrict_schedule = hide_schedule_information(request.user)
    )

    return render_to_response(
        template,
        data,
        context_instance=RequestContext(request),
    )



@permission_required_with_403('schedule.schedule_list')
def schedule_index(request, 
        year = datetime.now().strftime("%Y"), 
        month = datetime.now().strftime("%m"), 
        day = datetime.now().strftime("%d"), 
        template='schedule/schedule_daily.html',
        place = None,
        **params
    ):

    if place == None:
        # Possible to exist more than one place as matriz or none, filter and get first element
        if Place.objects.filter( place_type=1, organization=request.user.get_profile().org_active):
            place = Place.objects.filter(place_type=1, organization=request.user.get_profile().org_active)[0].id
        # non exist a matriz place
        else:
            place = Place.objects.filter(organization=request.user.get_profile().org_active)[0].id
    # Test if clinic administrator has registered referrals before access schedule page.
    if not Referral.objects.filter(status='01', organization=request.user.get_profile().org_active).count():
        return render_to_response('schedule/schedule_referral_alert.html', context_instance=RequestContext(request))

    return _datetime_view(request, template, datetime(int(year), int(month), int(day)), place, **params)



def week_view(request,
        year = datetime.now().strftime("%Y"), 
        month = datetime.now().strftime("%m"), 
        day = datetime.now().strftime("%d"),
    ):

    return render_to_response('schedule/schedule_week.html', dict(
                places = Place.objects.active().filter(organization=request.user.get_profile().org_active.id),
                rooms = Room.objects.active().filter(place__organization=request.user.get_profile().org_active.id),
                services = Service.objects.active().filter(organization=request.user.get_profile().org_active.id),
                professionals = CareProfessional.objects.active_all(request.user.get_profile().org_active.id),
                tab_week_class = 'active',
            ), context_instance=RequestContext(request))

def week_view_table(request,
    year = datetime.now().strftime("%Y"),
    month = datetime.now().strftime("%m"),
    day = datetime.now().strftime("%d"), ):

    if not year or not month or not day:
        today = datetime.now()
    else:
        today = datetime(year=int(year),month=int(month),day=int(day))

    first_week_day = today - timedelta(days=today.weekday())

    week = []
    occurrences = []
    occurrences_length = 0

    for i in range(7):
        occurrences_daily = []
        week_day = first_week_day+timedelta(i)
        week.append(week_day)
        groups = []
        for s in schedule_occurrences(request, week_day.strftime('%Y'), week_day.strftime('%m'), week_day.strftime('%d')):
            if s.is_group():
                if s.event.referral.group.pk not in groups:
                    occurrences_daily.append({
                        'is_group': True,
                        'group_name': u'%s' % s.event.referral.group,
                        'group_pk': s.event.referral.group.pk,
                        'data': s,
                    })
                    groups.append(s.event.referral.group.pk)
                    occurrences_length += 1

            else:
                occurrences_daily.append({
                    'is_group': False,
                    'data': s,
                })
                occurrences_length += 1

        occurrences.append(occurrences_daily)

    previous_week = today-timedelta(weeks=1)
    next_week = today+timedelta(weeks=1)
    last_week_day = first_week_day+timedelta(days=6)

    restrict_schedule = hide_schedule_information(request.user)

    return render_to_response('schedule/schedule_week_table.html', locals(), context_instance=RequestContext(request))



@permission_required_with_403('schedule.schedule_list')
def today_occurrences(request):
    return daily_occurrences(request, datetime.now().strftime("%Y"), datetime.now().strftime("%m"), datetime.now().strftime("%d"))



def schedule_occurrences(request, year = 1, month = 1, day = None):
    if day:
        date_start = datetime.strptime("%s%s%s" % (year, month, day),"%Y%m%d")
        date_end = date_start+timedelta(days=+1)
    else:
        date_start = datetime.strptime("%s%s" % (year, month),"%Y%m")
        date_end = date_start+timedelta( days=calendar.monthrange(int(year), int(month))[1] + 0)

    objs = ScheduleOccurrence.objects.filter(
            start_time__gte=date_start,
            start_time__lt=date_end,
            event__referral__organization=request.user.get_profile().org_active.id
            ).exclude(occurrenceconfirmation__presence = 4 # unmarked's
            ).exclude(occurrenceconfirmation__presence = 5 # remarked
            ).exclude(room__place__active = False # exclude not active places
            ).exclude(room__active = False) # exclude not active rooms

    return objs

@permission_required_with_403('schedule.schedule_list')
def daily_occurrences(request, year = 1, month = 1, day = None, place = None):

    #locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    #locale.setlocale(locale.LC_ALL,'en_US.UTF-8')
    #locale.setlocale(locale.LC_ALL,'pt_BR.ISO8859-1')
    occurrences = schedule_occurrences(request, year, month, day)

    array = {} #json
    i = 0
    groups = []

    date = datetime.strptime(('%s/%s/%s' % (year, month, day)), "%Y/%m/%d")

    if place == None:
        # Possible to exist more than one place as matriz or none, filter and get first element
        if Place.objects.filter( place_type=1, organization=request.user.get_profile().org_active):
            place = Place.objects.filter(place_type=1, organization=request.user.get_profile().org_active)[0].id
        # non exist a matriz place
        else:
            place = Place.objects.filter(organization=request.user.get_profile().org_active)[0].id

    array['util'] = {
        'date': ('%s-%s-%s' % (year, month, day)),
        'date_field': ('%s/%s/%s' % (year, month, day)),
        'str_date': u'%s, %s %s %s %s %s' % (date.strftime("%A").decode('utf-8'), date.strftime("%d"), _('of'), date.strftime("%B"), _('of'), date.strftime("%Y")),
        'next_day': (date + timedelta(days=+1)).strftime("%Y/%m/%d"),
        'prev_day': (date + timedelta(days=-1)).strftime("%Y/%m/%d"),
        'weekday': date.weekday(),
        'place': place,
    }

    for o in occurrences:
        have_same_group = False
        if hasattr(o.event.referral.group, 'id'):
            if '%s-%s-%s' % (o.event.referral.group.id, o.room_id, o.start_time.strftime('%H:%M:%S')) in groups:
                have_same_group = True

        if not have_same_group:
            range = o.end_time-o.start_time
            rowspan = range.seconds/1800 # how many blocks of 30min the occurrence have

            array[i] = {
                'id': o.id,
                'event_id': o.event.id,
                'room': o.room_id,
                'place': o.room.place_id,
                'room_name': (u"%s" % o.room),
                'service_id':o.event.referral.service.id,
                'group': (u"%s" % '' if not hasattr(o.event.referral.group, 'id') else o.event.referral.group.description),
                'group_id': '' if not hasattr(o.event.referral.group, 'id') else o.event.referral.group.id,
                'service': u"%s" % o.event.referral,
                'color':o.event.referral.service.color,
                'font_color':o.event.referral.service.font_color,
                'start_time': o.start_time.strftime('%H:%M:%S'),
                'end_time': o.end_time.strftime('%H:%M:%S'),
                'rowspan': rowspan,
                'online': o.is_online,
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

            sub_count = 0
            array[i]['device'] = {}

            if not o.scheduleoccurrence.was_confirmed():
                device_list = o.device.all()
            else:
                device_list = o.occurrenceconfirmation.device.all()

            for o in device_list:
                array[i]['device'][sub_count] = ({'id':o.id, 'name': ("%s - %s - %s" % (o.device.description, o.model, o.part_number)) })
                sub_count = sub_count + 1

            i = i + 1

            # concat group id, room id and start time to register in a list and verify in the begin of the loop if the same
            # occurrence already has been registered
            if hasattr(o, 'event') and hasattr(o.event.referral.group, 'id'):
                groups.append('%s-%s-%s' % (o.event.referral.group.id, o.room_id, o.start_time.strftime('%H:%M:%S')))

    array['util']['occurrences_total'] = i
    array = simplejson.dumps(array)

    return HttpResponse(array, mimetype='application/json')



@permission_required_with_403('schedule.schedule_write')
def occurrence_family_form(request, occurence_id = None, template=None):
    occurrence = get_object_or_404(ScheduleOccurrence, pk=occurence_id, event__referral__service__organization=request.user.get_profile().org_active)

    # check if requested user have perms to read it
    if not _access_check_by_occurrence(request, occurrence):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    if request.POST:
        if not request.POST.getlist('family_members'):
            messages.success(request, _('No member family selected'))
            return render_to_response(template, locals(), context_instance=RequestContext(request))

        if not hasattr(occurrence, 'occurrencefamily'):
            """ new register """
            f = OccurrenceFamily()
            f.occurrence_id = occurrence.id
            f.save()
        else:
            f = OccurrenceFamily.objects.get(occurrence=occurrence)

        for c in request.POST.getlist('family_members'):
            if c not in [x.id for x in f.client.all()]:
                f.client.add(c)

        messages.success(request, _('Family members added successfully'))
        return http.HttpResponseRedirect('/schedule/events/%s/family/form/' % occurrence.id)

    return render_to_response(template, locals(), context_instance=RequestContext(request))

@permission_required_with_403('schedule.schedule_write')
def occurrence_employee_form(request, occurence_id = None, template=None):
    occurrence = get_object_or_404(ScheduleOccurrence, pk=occurence_id, event__referral__service__organization=request.user.get_profile().org_active)

    # check if requested user have perms to read it
    if not _access_check_by_occurrence(request, occurrence):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    if request.POST:
        if not request.POST.getlist('company_employees'):
            messages.success(request, _('No company employees selected'))
            return render_to_response(template, locals(), context_instance=RequestContext(request))

        if not hasattr(occurrence, 'occurrenceemployees'):
            """ new register """
            f = OccurrenceEmployees()
            f.occurrence_id = occurrence.id
            f.save()
        else:
            f = OccurrenceEmployees.objects.get(occurrence=occurrence)

        for c in request.POST.getlist('company_employees'):
            if c not in [x.id for x in f.client.all()]:
                f.client.add(c)

        messages.success(request, _('Company employee(s) added successfully'))
        return http.HttpResponseRedirect('/schedule/events/%s/employee/form/' % occurrence.id)

    return render_to_response(template, locals(), context_instance=RequestContext(request))


@permission_required_with_403('schedule.schedule_write')
def schedule_settings(request):
    """
        Tiago de Souza Moraes
        Rodrigo Santana Gonçalves
        Save schedule settings, slot time, format display.
    """

    object = request.user.get_profile().org_active

    if request.POST:
        messages.success(request, _(u'Configuração da salvo com sucesso'))
        object.time_slot_schedule = request.POST.get('time_slot_schedule')
        object.restrict_schedule = request.POST.get('restrict_schedule')
        object.save()

    return render_to_response('schedule/schedule_settings.html', dict(
        object=object,
        time_slot_schedule=TIME_SLOT_SCHEDULE,
        tab_settings_class='active',
    ), context_instance=RequestContext(request))
