# -*- coding:utf-8 -*-

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
from datetime import datetime, timedelta, date
import datetime as datetime_

from django import http
from django.template.context import RequestContext
from django.shortcuts import get_object_or_404, render_to_response, HttpResponse
from django.utils.translation import ugettext as _
from django.utils import simplejson
from django.db.models import Q
from django.contrib import messages
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.template import Context

from swingtime.utils import create_timeslot_table, time_delta_total_seconds

from gestorpsi.referral.models import Referral
from gestorpsi.referral.forms import ReferralForm
from gestorpsi.place.models import Place, Room
from gestorpsi.service.models import Service, ServiceGroup
from gestorpsi.careprofessional.models import CareProfessional
from gestorpsi.client.models import Client

from gestorpsi.schedule.models import ScheduleOccurrence, OccurrenceConfirmation, OccurrenceFamily, OccurrenceEmployees
from gestorpsi.schedule.forms import ScheduleOccurrenceForm, ScheduleSingleOccurrenceForm, OccurrenceConfirmationForm

from gestorpsi.util.decorators import permission_required_with_403
from gestorpsi.util.views import get_object_or_None

from gestorpsi.financial.models import Receive
from gestorpsi.financial.forms import ReceiveFormUpdate, ReceiveFormNew
from gestorpsi.device.models import DeviceDetails
from gestorpsi.organization.models import TIME_SLOT_SCHEDULE, DEFAULT_SCHEDULE_VIEW
from gestorpsi.covenant.models import Covenant

import locale
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except:
    pass


def schedule_notify_email(org, occurrence, occurrence_confirmation):
    """
        to nofity by email a careprofessional if occurrence presence is 4 or 5
    """
    to = []
    oc_list = []
    oc_list.append(occurrence)

    if occurrence_confirmation.presence == 4:
        title = _('Occurrence unmarked')
    if occurrence_confirmation.presence == 5:
        title = _('Occurrence rescheduled')

    # emails address of all professional
    for p in occurrence.event.referral.professional.all():
        if p.person.notify.all() and p.person.notify.get(org_id=org.id).change_event:
            for e in p.person.emails.all():
                if not e.email in to:
                    to.append(e.email)

    if to:
        # render template
        text = Context({'oc_list':oc_list, 'title':title, 'org':org, 'showdt':True})
        template = get_template("schedule/schedule_notify_careprofessional.html").render(text)
        # sendmail
        msg = EmailMessage()
        msg.subject = u"GestorPsi - %s" % title
        msg.content_subtype = 'html'
        msg.encoding = "utf-8"
        msg.body = template
        msg.to = to
        msg.send()
        return True

    return False


def _access_check_by_occurrence(request, occurrence):
    from gestorpsi.client.views import _access_check
    denied_to_read = None
    for c in occurrence.event.referral.client.all():
        if not _access_check(request, c):
            denied_to_read = True

    if denied_to_read:
        return False

    return True


@permission_required_with_403('schedule.schedule_list')
def schedule_occurrence_listing(request, year=1, month=1, day=None, template='schedule/schedule_events.html', **extra_context):

    occurrences = schedule_occurrences(request, year, month, day)

    return render_to_response(
        template, 
        dict(
            extra_context, 
            occurrences=occurrences,
            places_list = Place.objects.active().filter(organization=request.user.get_profile().org_active.id),
            services = Service.objects.active().filter(organization=request.user.get_profile().org_active.id),
            professionals = CareProfessional.objects.active(request.user.get_profile().org_active.id),
            tab_event_class = 'active',
            ),
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
        recurrence_form_class=ScheduleOccurrenceForm,
        redirect_to = None
    ):

    disable_check_busy = False
    to_confirm_conflict = False  # dont show checkbox to ignore conflict

    # have to contains dtstart variable in URL. URL from schedule have to contains date and time data.
    if not 'dtstart' in request.GET:
        return http.HttpResponseRedirect('/schedule/')

    # get from url
    dtstart = parser.parse( request.GET['dtstart'] )
    room = get_object_or_None(Room, pk=request.GET.get('room'), place__organization=request.user.get_profile().org_active)
    client = get_object_or_None(Client, pk=request.GET.get('client'), person__organization=request.user.get_profile().org_active)
    referral = get_object_or_None(Referral, pk=request.GET.get('referral'), service__organization=request.user.get_profile().org_active)
    event_form = event_form_class

    if request.POST:
        if request.POST.get('ignore_conflict') == 'on':
            disable_check_busy = True

        # instance form
        recurrence_form = recurrence_form_class(request, room.place, request.POST)

        # no errors found, form is valid.
        if recurrence_form.is_valid():
            if not request.POST.get('group'): # booking single client
                referral = get_object_or_404(Referral, pk=request.POST.get('referral'), service__organization=request.user.get_profile().org_active)
                event_form = recurrence_form.save(referral, disable_check_busy=disable_check_busy)

            else: # booking a group
                group = get_object_or_404(ServiceGroup, pk=request.POST.get('group'), service__organization=request.user.get_profile().org_active, active=True)
                if group.charged_members(): # this check is already done in template. just to prevent empty groups
                    first = True
                    for group_member in group.charged_members():
                        if first:
                            event_form = recurrence_form.save(group_member.referral)
                            first = False
                        else:
                            if not event_form.errors:
                                event_form = recurrence_form.save(group_member.referral, True) # ignore busy check

            if not request.POST.get('group'): # booking single client
                '''
                    Create a payment for each upcoming event when event by pack or occurrence
                    Event per period will be created by script run by crontab everyday
                '''
                # check if occurrences have one payment by pack or event opened
                for o in referral.upcoming_nopayment_occurrences_():

                    # exist a payment for event?
                    if Receive.objects.filter(occurrence=o).count() == 0 :

                        # Filter payment by pack or occurrence
                        for x in referral.covenant.filter(Q(charge=1) | Q(charge=2) ).distinct():
                            receive = Receive() # new

                            """
                                by pack, by event.
                                charge2 overwrite charge1
                            """
                            # by pack
                            if x.charge == 2:
                                # check not terminated pack of same referral
                                for p in Receive.objects.filter(occurrence__event=event_form, covenant_charge=2):
                                    if not p.terminated_()[0]:
                                        # not terminated pack
                                        receive = p

                            # by occurrence
                            # new
                            if not receive.id:
                                receive.name = x.name
                                receive.price = x.price
                                receive.off = 0
                                receive.total = x.price
                                receive.covenant_charge = x.charge
                                receive.covenant_id = x.id
                                receive.save()

                                # by pack
                                receive.covenant_pack_size = x.event_time if x.charge == 2 else 0

                                # clear all
                                receive.covenant_payment_way_options = ''
                                for pw in x.payment_way.all():
                                    x = "(%s,'%s')," % ( pw.id , pw.name ) # need be a dict
                                    receive.covenant_payment_way_options += x

                            # add occurrence
                            receive.occurrence.add(o)
                            # update m2m
                            receive.save()

            if not event_form.errors:
                messages.success(request, _('Schedule saved successfully'))
                return http.HttpResponseRedirect(redirect_to or '/schedule/')
            else:
                messages.info(request, _(u'Conflito no agendamento.'))
                to_confirm_conflict = True  # show checkbox

    else:
        # mount form or return form errors
        # convert hour:minutes to second to set initial select
        interval_sec = time_delta_total_seconds( timedelta(minutes=int(request.user.get_profile().org_active.time_slot_schedule)) )
        start_sec = time_delta_total_seconds( timedelta(hours=dtstart.hour, minutes=dtstart.minute) )
        end_sec = start_sec + interval_sec

        recurrence_form = recurrence_form_class( request,
                                                 room.place, # start, end hour of place, render select in this range.
                                                 initial = dict(
                                                                dtstart=dtstart,
                                                                day=datetime.strptime(dtstart.strftime("%Y-%m-%d"), "%Y-%m-%d"),
                                                                until=datetime.strptime(dtstart.strftime("%Y-%m-%d"), "%Y-%m-%d"),
                                                                room=room.id,
                                                                start_time_delta=start_sec,
                                                                end_time_delta=end_sec,
                                                            )
        )

        recurrence_form.fields['device'].widget.choices = [(i.id, i) for i in DeviceDetails.objects.active(request.user.get_profile().org_active).filter(Q(room=room) | Q(mobility="2", lendable=True) | Q(place=room.place, mobility="2", lendable=False))]

    return render_to_response(template,
                               dict(
                                        slot_time = request.user.get_profile().org_active.time_slot_schedule,
                                        dtstart = dtstart, 
                                        event_form = event_form, 
                                        recurrence_form = recurrence_form, 
                                        group = ServiceGroup.objects.filter(service__organization = request.user.get_profile().org_active, active=True),
                                        room = room,
                                        object = client,
                                        referral = referral,
                                        room_id = room.id,
                                        disable_check_busy = disable_check_busy,
                                        to_confirm_conflict = to_confirm_conflict,
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
            recurrence_form = recurrence_form_class(request, request.POST)
            if recurrence_form.is_valid():
                recurrence_form.save(event)
                return http.HttpResponseRedirect(request.path)
        else:
            return http.HttpResponseBadRequest('Bad Request')

    event_form = event_form or event_form_class(instance=event)
    if not recurrence_form:
        recurrence_form = recurrence_form_class(
            request,
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

    occurrence = get_object_or_404(ScheduleOccurrence, pk=pk, event__pk=event_pk, event__referral__service__organization=request.user.get_profile().org_active)

    if request.method == 'POST':
        form = form_class(request.POST, instance=occurrence)

        if form.is_valid():
            form.save()
            messages.success(request, _('Occurrence updated successfully'))
            return http.HttpResponseRedirect(request.path)
    else:
        form = form_class(instance=occurrence, initial={'start_time':occurrence.start_time})
        form.fields['device'].queryset = DeviceDetails.objects.filter(Q(room = occurrence.room, mobility="1") | Q(place =  occurrence.room.place, room__place__organization = request.user.get_profile().org_active, mobility="2", lendable=False) | Q(room__place__organization = request.user.get_profile().org_active, mobility="2", lendable=True))

    return render_to_response(
        template,
        dict(occurrence=occurrence, form=form),
        context_instance=RequestContext(request)
    )



@permission_required_with_403('schedule.schedule_write')
def occurrence_confirmation_form_group(
        request, 
        pk, 
        template='schedule/schedule_occurrence_confirmation_form_group.html',
        form_class=OccurrenceConfirmationForm,
        client_id = None,
        redirect_to = None,
    ):

    '''
        confirmation event for a member of group
        choose a covenant of service and create a payment based in covenant
    '''

    occurrence = get_object_or_404(ScheduleOccurrence, pk=pk, event__referral__service__organization=request.user.get_profile().org_active)
    covenant_list = occurrence.event.referral.service.covenant.all().order_by('name')
    receive_list = []

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

    from gestorpsi.client.views import _access_check_referral_write
    denied_to_write = None

    if not _access_check_referral_write(request, occurrence.event.referral):
        denied_to_write = True

    # update occurrence and payments or new payment.
    if request.method == 'POST':

        # permission
        if denied_to_write:
            return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))


        # new payment form, not required.
        if not request.POST.get('select_covenant_receive') == '000' :

            covenant = Covenant.objects.get( pk=request.POST.get('select_covenant_receive'), organization=request.user.get_profile().org_active ) 
            pfx = 'receive_form---TEMPID999FORM' # hardcode Jquery 
            form_receive_new = ReceiveFormNew(request.POST, prefix=pfx, initial={ 'launch_date': date.today() })

            if form_receive_new.is_valid():

                fpn = form_receive_new.save()
                fpn.occurrence.add(occurrence)

                # from covenant
                fpn.covenant_payment_way_options = ''
                for pw in covenant.payment_way.all():
                    x = "(%s,'%s')," % ( pw.id , pw.name ) # need be a dict
                    fpn.covenant_payment_way_options += x

                fpn.covenant_payment_way_selected = request.POST.getlist('TEMPID999FORM-pw')
                fpn.save()


        # update payments, not required.
        for x in Receive.objects.filter(occurrence=occurrence):
            pfx = 'receive_form---%s' % x.id # hardcode Jquery 
            # new! fill payment date today
            if not x.launch_date:
                receive_list.append(ReceiveFormUpdate(request.POST, instance=x, prefix=pfx, initial={'launch_date':date.today()}))
            else:
                receive_list.append(ReceiveFormUpdate(request.POST, instance=x, prefix=pfx))

            if form_receive.is_valid():
                fp = form_receive.save()


        # occurrence
        form = form_class(request.POST, instance=occurrence_confirmation, initial={ 'device':initial_device, })

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

            messages.error(request, _(u'Campo inválido ou obrigatório'))

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

        # payments of occurrence, update form.
        for x in Receive.objects.filter(occurrence=occurrence):
            pfx = 'receive_form---%s' % x.id # for many forms and one submit.
            receive_list.append( ReceiveFormUpdate(instance=x, prefix=pfx) )


    # just one out if errors
    return render_to_response(
        template,
        dict(
                occurrence=occurrence,
                form=form,
                object=object,
                referral=occurrence.event.referral,
                occurrence_confirmation=occurrence_confirmation,
                hide_date_field=True if occurrence_confirmation and int(occurrence_confirmation.presence) > 2 else None,
                denied_to_write = denied_to_write,
                receive_list = receive_list,
                covenant_list = covenant_list,
                receive_new_form = ReceiveFormNew(prefix='receive_form---TEMPID999FORM'),
            ),
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

    '''
        confirmation event
    '''

    occurrence = get_object_or_404(ScheduleOccurrence, pk=pk, event__referral__service__organization=request.user.get_profile().org_active)
    receive_list = []
    
    if not occurrence.scheduleoccurrence.was_confirmed():
        initial_device = [device.pk for device in occurrence.device.all()]
    else:
        initial_device = [device.pk for device in occurrence.occurrenceconfirmation.device.all()]
        
    # check if requested user have perms to read it
    if not _access_check_by_occurrence(request, occurrence):
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    try:
        occurrence_confirmation = OccurrenceConfirmation.objects.get(pk=occurrence.occurrenceconfirmation.id)
    except:
        occurrence_confirmation = None
    
    object = get_object_or_None(Client, pk=client_id, person__organization=request.user.get_profile().org_active)

    from gestorpsi.client.views import _access_check_referral_write
    denied_to_write = None

    if not _access_check_referral_write(request, occurrence.event.referral):
        denied_to_write = True

    if request.method == 'POST':

        if denied_to_write:
            return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

        form = form_class(request.POST, instance=occurrence_confirmation, initial={'device':initial_device})

        # receive
        payment_valid = True

        for x in Receive.objects.filter(occurrence=occurrence):

            pfx = 'receive_form---%s' % x.id # hardcode Jquery 
            form_receive = ReceiveFormUpdate(request.POST, instance=x, prefix=pfx)

            receive_list.append(form_receive)

            if form_receive.is_valid():
                fp = form_receive.save()
            else:
                payment_valid = False

        # occurrence
        if form.is_valid() and payment_valid :

            occurrence_confirmation = form.save(commit=False)
            occurrence_confirmation.occurrence = occurrence

            if int(occurrence_confirmation.presence) not in (1,2): # client not arrive, dont save datetime field
                occurrence_confirmation.date_started = None
                occurrence_confirmation.date_finished = None

            occurrence_confirmation.save()
            form.save_m2m()

            # save occurrence comment
            occurrence.annotation = request.POST['occurrence_annotation']
            occurrence.save()

            # sendmail for careprofessional when presence is 4 or 5
            if hasattr(occurrence_confirmation,'presence'):
                if occurrence_confirmation.presence == 4 or occurrence_confirmation.presence == 5 :
                    schedule_notify_email(request.user.get_profile().org_active, occurrence, occurrence_confirmation)

            messages.success(request, _('Occurrence confirmation updated successfully'))
            return http.HttpResponseRedirect(redirect_to or request.path)

        else:
            form.fields['device'].widget.choices = [(i.id, i) for i in DeviceDetails.objects.active(request.user.get_profile().org_active).filter(Q(room=occurrence.room) | Q(mobility=2, lendable=True) | Q(place = occurrence.room.place, mobility=2, lendable=False))]
            messages.error(request, _(u'Campo inválido ou obrigatório'))

    # not request.POST
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

        # payment form
        for x in Receive.objects.filter(occurrence=occurrence):
            pfx = 'receive_form---%s' % x.id

            # new! fill payment date today
            if not x.launch_date:
                receive_list.append( ReceiveFormUpdate(instance=x, prefix=pfx, initial={ 'launch_date':date.today() }) )
            else:
                receive_list.append( ReceiveFormUpdate(instance=x, prefix=pfx) )

    return render_to_response(
        template,
        dict(
                occurrence=occurrence,
                form=form,
                object=object,
                referral=occurrence.event.referral,
                occurrence_confirmation=occurrence_confirmation,
                hide_date_field=True if occurrence_confirmation and int(occurrence_confirmation.presence) > 2 else None,
                denied_to_write = denied_to_write,
                receive_list = receive_list,
            ),
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

    user = request.user
    timeslot_factory = timeslot_factory or create_timeslot_table

    params = params or {}
    data = dict(

        day=dt, 
        next_day=dt + timedelta(days=+1),
        prev_day=dt + timedelta(days=-1),

        # get start_time and end_time_delta from place
        # get schedule slot time from organization
        timeslots=timeslot_factory(
                dt,\
                items,\
                start_time=datetime_.time( place.hours_work()[0], place.hours_work()[1]),\
                end_time_delta=timedelta(hours=place.hours_work()[2] ),\
                time_delta=timedelta( minutes=int(user.get_profile().org_active.time_slot_schedule) ),\
                **params),

        places_list = Place.objects.active().filter(organization=request.user.get_profile().org_active.id),
        place = place,
        place_id = place.id,

        services = Service.objects.active().filter(organization=request.user.get_profile().org_active.id),
        professionals = CareProfessional.objects.active_all(request.user.get_profile().org_active.id),
        referral = referral,
        object = object,
        tab_daily_class = "active", # class object, tab menu
    )

    return render_to_response(
        template,
        data,
        context_instance=RequestContext(request),
    )


@permission_required_with_403('schedule.schedule_list')
def schedule_index(request):

    if request.user.get_profile().org_active.default_schedule_view == '0':
        return http.HttpResponseRedirect('/schedule/diary/')

    if request.user.get_profile().org_active.default_schedule_view == '1':
        return http.HttpResponseRedirect('/schedule/week/')

    if request.user.get_profile().org_active.default_schedule_view == '2':
        return http.HttpResponseRedirect('/schedule/events/')


@permission_required_with_403('schedule.schedule_list')
def diary_view(request, 
        year = datetime.now().strftime("%Y"), 
        month = datetime.now().strftime("%m"), 
        day = datetime.now().strftime("%d"), 
        place=None,
        template='schedule/schedule_daily.html',
        **params
    ):

    if place == None:
        # Possible to exist more than one place as matriz or none, filter and get first element
        if Place.objects.filter( place_type=1, organization=request.user.get_profile().org_active):
            place = Place.objects.filter(place_type=1, organization=request.user.get_profile().org_active)[0].id
        # non exist a matriz place
        else:
            place = Place.objects.filter(organization=request.user.get_profile().org_active)[0].id
    
    places_list = Place.objects.active().filter(organization=request.user.get_profile().org_active.id)

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
                places_list = Place.objects.active().filter(organization=request.user.get_profile().org_active.id),
                rooms = Room.objects.active().filter(place__organization=request.user.get_profile().org_active.id),
                services = Service.objects.active().filter(organization=request.user.get_profile().org_active.id),
                professionals = CareProfessional.objects.active_all(request.user.get_profile().org_active.id),
                tab_week_class = 'active',
                place = Place.objects.filter(place_type=1, organization=request.user.get_profile().org_active)[0],
            ), context_instance=RequestContext(request))


def week_view_table(request,
        year = datetime.now().strftime("%Y"), 
        month = datetime.now().strftime("%m"), 
        day = datetime.now().strftime("%d"), 
    ):

    if not year or not month or not day:
        today = datetime.now()
    else:
        today = datetime(year=int(year),month=int(month),day=int(day))
    
    first_week_day = today - timedelta(days=today.weekday())

    week = []
    schedule = []
    '''
    schedule array
        schedule = [ [period] ]
            period = [ [period_list], occurrence_total , [days-week] ]
                occurrence_total = total of occurrence of period; integer
                    days-week = [ [monday] , ... , [sunday] ]
                        monday = [occurrences objects]
    
    '''
    occurrences_length_total = 0 # show resume top page

    '''
     period of day
     array format
             [0] = label
             [1] = start time hour
             [2] = start time minute
             [3] = end time hour
             [4] = end time minute
             [5] = color
    '''
    period_list = []
    period_list.append([u'Manhã 00:00 - 12:00',00,00,12,00,'green'])   # manha
    period_list.append([u'Tarde 12:00 - 18:00',12,00,18,00,'orange'])  # tarde
    period_list.append([U'Noite 18:00 - 24:00',18,00,23,59,'blue'])    # noite
    
    # for each period
    for t in period_list:

        occurrences_length = 0 # show resume per period
        day = [] # array of days of week / new day
        period = [] # a new period
        period.append(t) # 0 / add label; time; color;
        period.append(0) # 1 / total of occurrences of this period

        # week day
        for i in range(7):

            week_day = first_week_day+timedelta(i)

            if not week_day in week:
                week.append(week_day)

            # all occurrences of day
            groups = []
            occurrence = [] # occurrences of day

            for s in schedule_occurrences(request, week_day.strftime('%Y'), week_day.strftime('%m'), week_day.strftime('%d'), t[1], t[2], t[3], t[4]):
                if s.is_group():
                    if s.event.referral.group.pk not in groups:
                        occurrence.append({
                            'is_group': True,
                            'group_name': u'%s' % s.event.referral.group,
                            'group_pk': s.event.referral.group.pk,
                            'data': s,
                            'show': show_event_(request, s),
                        })
                        groups.append(s.event.referral.group.pk)
                        
                else:
                    occurrence.append({
                        'is_group': False,
                        'data': s,
                        'show': show_event_(request, s),
                    })

                occurrences_length += 1 # show resume top page
                occurrences_length_total += 1 # total of occurrences of week

            period[1] = occurrences_length # update occurrences counter of period

            day.append(occurrence) # occurrence of day
            period.append(day) # day of period
        schedule.append(period) # period of schedule

    previous_week = today-timedelta(weeks=1)
    next_week = today+timedelta(weeks=1)
    last_week_day = first_week_day+timedelta(days=6)

    return render_to_response('schedule/schedule_week_table.html', locals(), context_instance=RequestContext(request))



@permission_required_with_403('schedule.schedule_list')
def today_occurrences(request):
    return daily_occurrences(request, datetime.now().strftime("%Y"), datetime.now().strftime("%m"), datetime.now().strftime("%d"))



def schedule_occurrences(request, year=1, month=1, day=None, st_timeh=00, st_timem=00, ed_timeh=23, ed_timem=59):
    '''
        st_timeh = start time hour : integer
        st_timem = start time minute : integer
        ed_timeh = end time hour : integer
        ed_timem = end time minute : integer
    '''

    if day:
        date_start = datetime.strptime("%s%s%s%s%s" % (year, month, day, st_timeh, st_timem),"%Y%m%d%H%M")
        date_end = datetime.strptime("%s%s%s%s%s" % (year, month, day, ed_timeh, ed_timem),"%Y%m%d%H%M")
    else:
        date_start = datetime.strptime("%s%s" % (year, month),"%Y%m")
        date_end = date_start+timedelta( days=calendar.monthrange(int(year), int(month))[1] + 0)

    objs = ScheduleOccurrence.objects.filter(
            start_time__gte=date_start,
            start_time__lt=date_end,
            event__referral__organization=request.user.get_profile().org_active
            ).exclude(occurrenceconfirmation__presence = 4 # unmarked's
            ).exclude(occurrenceconfirmation__presence = 5 # remarked
            ).exclude(room__place__active = False # exclude not active places
            ).exclude(room__active = False) # exclude not active rooms

    return objs


def show_event_(request, o):
    """
        Show all information about event.
        boolean :   True 
                    or
                    False (show as reserved)
    """

    full_data = False # show all information or reserved

    if request.user.profile.person.is_secretary() or request.user.profile.person.is_administrator():
        full_data = True

    # logged careprofessional or student in professional list
    if request.user.profile.person.is_careprofessional() and request.user.get_profile().person.careprofessional in o.event.referral.professional.all():
        full_data = True

    if request.user.profile.person.is_student() and request.user.get_profile().person.careprofessional in o.event.referral.professional.all():
        full_data = True

    return full_data


@permission_required_with_403('schedule.schedule_list')
def daily_occurrences(request, year=1, month=1, day=None, place=None):
    """
        return JSON
        filter permission : professional or secretary
    """
    occurrences = schedule_occurrences(request, year, month, day)

    i = 0
    groups = []
    array = {} #json

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
        u'str_date': '%s, %s %s %s %s %s' % (date.strftime("%A").decode('utf-8').capitalize(), date.strftime("%d"), _('of'), date.strftime("%B").decode('utf-8'), _('of'), date.strftime("%Y")),
        'next_day': (date + timedelta(days=+1)).strftime("%Y/%m/%d"),
        'prev_day': (date + timedelta(days=-1)).strftime("%Y/%m/%d"),
        'weekday': date.weekday(),
        'place': place,
    }
    
    """
        secretary and/or admin
            see all occurrences
        professional and/or student
            see event if owner of it OR reservado
    """
    # to check each occurence permission
    for o in occurrences:

        have_same_group = False
        if hasattr(o.event.referral.group, 'id'):
            if '%s-%s-%s' % (o.event.referral.group.id, o.room_id, o.start_time.strftime('%H:%M:%S')) in groups:
                have_same_group = True

        if not have_same_group:
            range = o.end_time-o.start_time
            rowspan = range.seconds/time_delta_total_seconds( timedelta(minutes=int(request.user.get_profile().org_active.time_slot_schedule)) ) 

        if show_event_(request, o): # to show full data
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
        else: # to show as reservado
            array[i] = {
                'room': o.room_id,
                'room_name': (u"%s" % o.room),
                'place': o.room.place_id,
                'group': u"",
                'service': "RESERVADO",
                'service_id':o.event.referral.service.id,
                'color':o.event.referral.service.color,
                'font_color':o.event.referral.service.font_color,
                'start_time': o.start_time.strftime('%H:%M:%S'),
                'end_time': o.end_time.strftime('%H:%M:%S'),
                'rowspan': rowspan,
            }
        
        array[i]['professional'] = {}
        array[i]['client'] = {}
        array[i]['device'] = {}

        if show_event_(request, o): # to show full data

            sub_count = 0
            for p in o.event.referral.professional.all():
                array[i]['professional'][sub_count] = ({'id':p.id, 'name':p.person.name})
                sub_count = sub_count + 1

            sub_count = 0
            for c in o.event.referral.client.all():
                array[i]['client'][sub_count] = ({'id':c.id, 'name':c.person.name})
                sub_count = sub_count + 1
        
            sub_count = 0
            if not o.scheduleoccurrence.was_confirmed():
                device_list = o.device.all()
            else:
                device_list = o.occurrenceconfirmation.device.all()

            for o in device_list:
                array[i]['device'][sub_count] = ({'id':o.id, 'name': ("%s - %s - %s" % (o.device.description, o.brand, o.model)) })
                sub_count = sub_count + 1

            # concat group id, room id and start time to register in a list and verify in the begin of the loop if the same
            # occurrence already has been registered
            if hasattr(o, 'event') and hasattr(o.event.referral.group, 'id'):
                groups.append('%s-%s-%s' % (o.event.referral.group.id, o.room_id, o.start_time.strftime('%H:%M:%S')))

        i = i + 1

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
            messages.error(request, _('No member family selected'))
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
            messages.error(request, _('No company employees selected'))
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
        Save schedule settings, slot time, format display.
    """

    # organization
    object = request.user.get_profile().org_active

    if request.POST:

        object.default_schedule_view = request.POST.get('default_schedule_view')
        messages.success(request, _(u'Configuração gravada com sucesso!'))

        if not object.time_slot_schedule == request.POST.get('time_slot_schedule'):
            object.time_slot_schedule = request.POST.get('time_slot_schedule')
            messages.info(request, _(u'Com a alteração do intervalo, alguns eventos podem não aparecer na agenda diária devido a nova grade de horário.'))

        object.save()

    return render_to_response('schedule/schedule_settings.html', dict(
                object = object,
                time_slot_schedule = TIME_SLOT_SCHEDULE,
                default_schedule_view = DEFAULT_SCHEDULE_VIEW,
                tab_settings_class = 'active',
                places_list = Place.objects.active().filter(organization=request.user.get_profile().org_active.id),
            ), context_instance=RequestContext(request) )
