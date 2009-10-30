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

from django.conf.urls.defaults import *
from gestorpsi.referral.forms import ReferralForm
from gestorpsi.schedule.forms import ScheduleOccurrenceForm, ScheduleSingleOccurrenceForm, OccurrenceConfirmationForm
from gestorpsi.schedule.views import occurrence_view
from gestorpsi.schedule.views import add_event
from gestorpsi.schedule.views import schedule_index
from gestorpsi.schedule.views import schedule_occurrence_listing_today
from gestorpsi.schedule.views import event_view
from gestorpsi.schedule.views import daily_occurrences 
from gestorpsi.schedule.views import today_occurrences
from gestorpsi.schedule.views import occurrence_confirmation_form
from gestorpsi.schedule.views import occurrence_family_form

urlpatterns = patterns('',
     url(
        r'^(?:calendar/)?$', 
        schedule_index, 
        name='schedule-index'
    ),
    url(
        r'^occurrences/(\d{4})/(0?[1-9]|1[012])/([0-3]?\d)/$', 
        daily_occurrences,
        name='schedule-daily-occurrences'
    ),
    url(
        r'^occurrences/$', 
        today_occurrences,
        name='schedule-today-occurrences'
    ),
    url(
        r'^events/$',
        schedule_occurrence_listing_today,
        { 'template': 'schedule/schedule_events.html', },
        name='schedule-events-today'
    ),
    url(
        r'^events/add/$', 
        add_event, 
        {
            'event_form_class': ReferralForm ,
            'recurrence_form_class': ScheduleOccurrenceForm ,
            'template': 'schedule/schedule_form.html',
        },
        name='swingtime-add-event',
        
    ),
    url(
        r'^events/(\d+)/$', 
        event_view,
        {
            'event_form_class': ReferralForm ,
            'recurrence_form_class': ScheduleOccurrenceForm ,
            'template': 'schedule/event_detail.html',
        },       
        name='swingtime-event'
    ),
    url(
        r'^events/(\d+)/(\d+)/$',
        occurrence_view,
        {'template':'schedule/schedule_occurrence_form.html',
         'form_class': ScheduleSingleOccurrenceForm,
        },
        name='swingtime-occurrence'
    ),
    
    url(
        r'^events/(\d+)/confirmation/$', 
        occurrence_confirmation_form, 
        {'template':'schedule/schedule_occurrence_confirmation_form.html',
         'form_class': OccurrenceConfirmationForm,
        },
        name='swingtime-occurrence-confirmation'
    ),
    url(
        r'^events/(\d+)/family/form/$', 
        occurrence_family_form, 
        {'template':'schedule/schedule_occurrence_family_form.html',
         #'form_class': OccurrenceConfirmationForm,
        },
        name='swingtime-occurrence-family-form'
    ),
    
)
