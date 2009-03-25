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
from django.views.generic.simple import direct_to_template
from swingtime.views import occurrence_view
from gestorpsi.referral.forms import ReferralForm
from gestorpsi.schedule.forms import ScheduleOccurrenceForm
from gestorpsi.schedule.views import add_event, schedule_index, schedule_occurrence_listing, schedule_occurrence_listing_today, event_view, daily_occurrences, today_occurrences
#from gestorpsi.schedule.views import calendar_view

urlpatterns = patterns('',
    #url(r'^$', direct_to_template, { 'template': 'schedule/schedule_index.html'}, name='schedule-home'),
#    url(r'^swingtime/events/type/([^/]+)/$', 'event_type', name='karate-event'),
    
     #url(
        #r'^(?:calendar/)?$', 
        #calendar_view, 
        #{ 'template': 'schedule/daily_view.html', },
        #name='swingtime-today'
    #),
    
     url(
        r'^(?:calendar/)?$', 
        schedule_index, 
        name='schedule-index'
    ),
    #url(
        #r'^calendar/(\d{4})/(0?[1-9]|1[012])/([0-3]?\d)/$', 
        #calendar_view,
        #{ 'template':'schedule/daily_view.html', },
        #name='swingtime-daily-view'
    #),
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
        r'^events/(\d{4})/(0?[1-9]|1[012])/([0-3]?\d)/$',
        schedule_occurrence_listing,
        name='schedule-listing-daily'
    ),
    url(
        r'^events/(\d{4})/(0?[1-9]|1[012])/$',
        schedule_occurrence_listing,
        name='schedule-listing-monthly'
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
        {'template':'schedule/schedule_occurrence.html'},
        name='swingtime-occurrence'
    ),
    
        #url(
        #r'^events/(\d+)/$', 
        #event_view, 
        #name='swingtime-event'
    #),
    
    #url(
        #r'^events/(\d+)/(\d+)/$', 
        #occurrence_view, 
        #name='swingtime-occurrence'
    #),
    
)
