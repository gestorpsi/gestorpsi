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

from datetime import datetime, date, time, timedelta
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import ugettext as _
from swingtime.forms import MultipleOccurrenceForm, SingleOccurrenceForm
from swingtime import utils
from gestorpsi.schedule.models import ScheduleOccurrence, OccurrenceConfirmation
from gestorpsi.place.models import Room
from gestorpsi.device.models import DeviceDetails
from gestorpsi.schedule import settings as swingtime_settings
from gestorpsi.util.widgets import SplitSelectDateTimeWidget
from gestorpsi.schedule.models import OCCURRENCE_CONFIRMATION_PRESENCE 

def timeslot_offset_options(
    type=False,
    interval=False,
    start_time=False,
    end_time=False,
    fmt=swingtime_settings.TIMESLOT_TIME_FORMAT,
):
    '''
    Create a list of time slot options for use in swingtime forms.
    
    The list is comprised of 2-tuples containing the number of seconds since the
    start of the day and a 12-hour temporal representation of that offset.

    type : string start or end
    interval : int 
    start_time : string format 08:45 or 08:00
    end_time : string format 20:45 or 20:00
    
    '''
    dt = datetime.combine(date.today(), time(0))
    interval = timedelta(minutes=interval)

    H,M = start_time.split(",")
    dtstart = datetime.combine(dt.date(), time(int(H), int(M)) )

    H,M = end_time.split(",")
    dtend = datetime.combine(dt.date(), time(int(H), int(M)) )

    options = []
    delta = utils.time_delta_total_seconds(dtstart - dt)
    seconds = utils.time_delta_total_seconds(interval)

    while dtstart <= dtend:
        options.append((delta, dtstart.strftime('%H:%M')))
        dtstart += interval
        delta += seconds

    if type == 'start': # remove last
        del options[-1]

    if type == 'end': # remove first
        del options[0]

    return options


class SplitDateTimeWidget(forms.MultiWidget):
    '''
    A Widget that splits datetime input into a SelectDateWidget for dates and
    Select widget for times.
    
    '''
    def __init__(self, attrs=None):
        widgets = (
            SelectDateWidget(attrs=attrs), 
            forms.Select(choices=default_timeslot_options, attrs=attrs)
        )
        super(SplitDateTimeWidget, self).__init__(widgets, attrs)


    def decompress(self, value):
        if value:
            return [value.date(), value.time().replace(microsecond=0)]
        
        return [None, None]


class ScheduleSingleOccurrenceForm(SingleOccurrenceForm):
    room = forms.ModelChoiceField(queryset=Room.objects.all(), widget=forms.Select(attrs={'class':'extramedium asm', }))
    device = forms.ModelMultipleChoiceField(required = False, queryset=DeviceDetails.objects.all(), widget=forms.SelectMultiple(attrs={'class':'multiselectable', }))
    annotation = forms.CharField(required = False, widget=forms.Textarea(attrs={'class':'giant'}))
    
    class Meta:
        model = ScheduleOccurrence


class ScheduleOccurrenceForm(MultipleOccurrenceForm):
    room = forms.ModelChoiceField(queryset=Room.objects.all(), widget=forms.Select(attrs={'class':'extramedium asm', }))
    device = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices = (
        [(i.id, i) for i in DeviceDetails.objects.all()]
        ))    
    annotation = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'giant','rows':'10'}))
    is_online = forms.BooleanField(required = False)

    class Meta:
        model = ScheduleOccurrence


    def __init__(self, request, place, *args, **kwargs):
        """
            request: request
            place: Place()
                get start, end hour of place
        """
        super(ScheduleOccurrenceForm, self).__init__(*args, **kwargs)

        # rewrite slot time based in the settings of organization schedule
        self.fields['start_time_delta'] = forms.IntegerField(
            label='Start time',
            widget=forms.Select(choices=timeslot_offset_options('start', int(request.user.get_profile().org_active.time_slot_schedule), place.hour_start, place.hour_end)) 
            )
        
        # rewrite slot time based in the settings of organization schedule
        self.fields['end_time_delta'] = forms.IntegerField(
            label='End time',
            widget=forms.Select(choices=timeslot_offset_options('end', int(request.user.get_profile().org_active.time_slot_schedule), place.hour_start, place.hour_end)) 
        )

    def save(self, event, disable_check_busy=False):
        if self.cleaned_data['repeats'] == 'no':
            params = {}
        else:
            params = self._build_rrule_params()

        import logging
        logging.debug("is online: " + str(self.cleaned_data['is_online']))

        event.errors = event.add_occurrences(
            self.cleaned_data['start_time'], 
            self.cleaned_data['end_time'],
            self.cleaned_data['room'].id,
            self.cleaned_data['device'],
            self.cleaned_data['annotation'],
            self.cleaned_data['is_online'],
            disable_check_busy,
            **params
        )

        return event


class OccurrenceConfirmationForm(forms.ModelForm):
    presence = forms.CharField(label=_('Presence'), required=True, widget=forms.RadioSelect(choices=OCCURRENCE_CONFIRMATION_PRESENCE, attrs={'required':'required'}) )
    date_started = forms.DateTimeField(label=_('Time Started'), required=False, widget=SplitSelectDateTimeWidget(minute_step=5))
    date_finished = forms.DateTimeField(label=_('Time Finished'), required=False, widget=SplitSelectDateTimeWidget(minute_step=5))
    device = forms.MultipleChoiceField(label=_('Devices utilized in this session'), required=False, widget=forms.CheckboxSelectMultiple, choices = (
        [(i.id, i) for i in DeviceDetails.objects.all()]
        ))   
    reason = forms.CharField(label=_('Unmark or Reschedule Reason (if exists)'), required = False, widget=forms.Textarea(attrs={'class':'giant'}))
    anotation = forms.CharField(label=_('Anotation'), required = False, widget=forms.Textarea(attrs={'class':'giant'}))

    def __init__(self, *args, **kwargs):
        super(OccurrenceConfirmationForm, self).__init__(*args, **kwargs)
        self.initial.setdefault('date_started', self.initial.get('start_time'))
        self.initial.setdefault('date_finished', self.initial.get('end_time'))
        self.initial.setdefault('occurrence', self.initial.get('occurrence'))
        self.fields['presence'].required = True

    class Meta:
        model = OccurrenceConfirmation
        fields = ('date_started', 'date_finished', 'presence', 'reason', 'device')
