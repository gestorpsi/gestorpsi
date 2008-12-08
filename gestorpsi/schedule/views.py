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

def index(request):
    today = datetime.datetime.now()
    cal = calendar.HTMLCalendar(calendar.SUNDAY)
    month = calendar.monthcalendar(today.year, today.month)
#    print c.formatmonth(2008, 04)
    return render_to_response('schedule/schedule_index.html', locals())