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

from django import forms
from swingtime.forms import MultipleOccurrenceForm
from gestorpsi.schedule.models import ScheduleOccurrence
from gestorpsi.place.models import Room
from gestorpsi.device.models import DeviceDetails

class ScheduleOccurrenceForm(MultipleOccurrenceForm):
    room = forms.ModelChoiceField(queryset=Room.objects.all(), widget=forms.Select(attrs={'class':'extramedium asm', }))
    device = forms.ModelMultipleChoiceField(required = False, queryset=DeviceDetails.objects.mobile(), widget=forms.SelectMultiple(attrs={'class':'extrabig multiple asm', }))
    annotation = forms.CharField(required = False, widget=forms.Textarea())
    
    class Meta:
        model = ScheduleOccurrence

    def save(self, event):
        if self.cleaned_data['repeats'] == 'no':
            params = {}
        else:
            params = self._build_rrule_params()

        event.add_occurrences(
            self.cleaned_data['start_time'], 
            self.cleaned_data['end_time'],
            self.cleaned_data['room'].id,
            **params
        )

        return event

