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
from gestorpsi.authentication.views import login_check
from gestorpsi.referral.forms import ReferralForm
from gestorpsi.schedule.forms import ScheduleOccurrenceForm, ScheduleSingleOccurrenceForm, OccurrenceConfirmationForm

from gestorpsi.schedule.views import occurrence_view, schedule_settings, add_event, schedule_index, schedule_occurrence_listing_today, event_view, daily_occurrences, today_occurrences, occurrence_confirmation_form, occurrence_family_form, occurrence_employee_form, occurrence_group, week_view, week_view_table

urlpatterns = patterns('',
    url(
        r'^(?:calendar/)?$', 
        login_check(schedule_index), 
        name='schedule-index'
    ),

    # set schedule slot time
    url(
        r'^settings/$', 
        login_check(schedule_settings), 
        name='schedule-settings'
    ),

    # index, not default place
     url(
        r'^place/(?P<place>([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}))/$', 
        login_check(schedule_index), 
        name='schedule-index'
    ),
    
    # return JSON
    url(
        r'^occurrences/(?P<year>(\d)+)/(?P<month>(\d)+)/(?P<day>(\d)+)/place/(?P<place>([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}))/$', 
        login_check(daily_occurrences),
        name='schedule-daily-occurrences'
    ),
    url(
        r'^occurrences/$', 
        login_check(today_occurrences),
        name='schedule-today-occurrences'
    ),
    url(
        r'^events/$',
        login_check(schedule_occurrence_listing_today),
        { 'template': 'schedule/schedule_events.html', },
        name='schedule-events-today'
    ),
    url(
        r'^events/add/$', 
        login_check(add_event), 
        {
            'event_form_class': ReferralForm ,
            'recurrence_form_class': ScheduleOccurrenceForm ,
            'template': 'schedule/schedule_form.html',
        },
        name='swingtime-add-event',
        
    ),
    url(
        r'^events/(\d+)/$', 
        login_check(event_view),
        {
            'event_form_class': ReferralForm ,
            'recurrence_form_class': ScheduleOccurrenceForm ,
            'template': 'schedule/event_detail.html',
        },       
        name='swingtime-event'
    ),
    url(
        r'^events/(\d+)/(\d+)/$',
        login_check(occurrence_view),
        {'template':'schedule/schedule_occurrence_form.html',
         'form_class': ScheduleSingleOccurrenceForm,
        },
        name='swingtime-occurrence'
    ),
    url(
        r'^week/$', 
        login_check(week_view),
        name='swingtime-week'
    ),
    url(
        r'^week/(\d{4})/(0?[1-9]|1[012])/([0-3]?\d)/$', 
        login_check(week_view_table),
        name='swingtime-week-table'
    ),
    url(
        r'^week/today/$', 
        login_check(week_view_table),
        name='swingtime-week-table'
    ),
    url(
        r'^events/(\d+)/confirmation/$', 
        login_check(occurrence_confirmation_form), 
        {'template':'schedule/schedule_occurrence_confirmation_form.html',
         'form_class': OccurrenceConfirmationForm,
        },
        name='swingtime-occurrence-confirmation'
    ),
    url(
        r'^events/group/(?P<group_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/occurrence/(?P<occurrence_id>\d+)/$', 
        login_check(occurrence_group), 
        {'template':'schedule/schedule_occurrence_group.html',
         #'form_class': OccurrenceConfirmationForm,
        },
        name='swingtime-occurrence-group'
    ),
    url(
        r'^events/(\d+)/family/form/$', 
        login_check(occurrence_family_form), 
        {'template':'schedule/schedule_occurrence_family_form.html',
         #'form_class': OccurrenceConfirmationForm,
        },
        name='swingtime-occurrence-family-form'
    ),
    url(
        r'^events/(\d+)/employee/form/$', 
        login_check(occurrence_employee_form), 
        {'template':'schedule/schedule_occurrence_employee_form.html',
         #'form_class': OccurrenceConfirmationForm,
        },
        name='swingtime-occurrence-employee-form'
    ),
    
)
