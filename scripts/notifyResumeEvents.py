#!/usr/bin/env python
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

'''
    script used to send the resume of events of day for professional
'''

import header

from datetime import date, timedelta
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.template import Context

from gestorpsi.schedule.models import Occurrence
from django.conf import settings

# check if exist events of next day for all professionals
dt = date.today() + timedelta(settings.NOTIFY_EVENTS_PROFESSIONAL) # correct

# main code
week_days = (u'Segunda-feira', u'Terça-feira', u'Quarta-feira', u'Quinta-feira', u'Sexta-feira', u'Sábado', u'Domingo')
d = dt.day
m = dt.month
y = dt.year

# sent professional list
sent = [] # store professional.id + org.id : "12345+abcde"

# all occurrence of next day

"""
    to check:
        all events 
            all professional of each event
                all orgs of each professional
                    if notify settings is true for this org
                        send by email the resume of events of this org of next day
"""
#for oc in Occurrence.objects.filter(start_time__year=y, start_time__month=m, start_time__day=d, event__referral__organization__id='bcbfdb8e-1641-4478-9e7c-3e0f1befbede'): # debug/test
for oc in Occurrence.objects.filter(start_time__year=y, start_time__month=m, start_time__day=d): # correct
    # for each professional
    for pr in oc.event.referral.professional.all():
        # for each org of professional
        for org in pr.person.organization.all():

            k = u"%s+++%s" % (pr.id, org.id)
            to = []
            oc_list = [] # occurrence list

            # professional whant to receive resume occurrences of next day by email?
            if pr.person.notify.filter(org_id=org.id) and pr.person.notify.get(org_id=org.id).resume_daily_event and k not in sent:
                sent.append(k) # to check professional, avoid duplicate

                for x in pr.person.emails.all():
                    to.append(u'%s' % x.email)

                # list of occurrence of professional in day, exclude unmarked and rescheduled.
                for x in Occurrence.objects.filter(start_time__year=y, start_time__month=m, start_time__day=d,event__referral__professional=pr,\
                        event__referral__organization=org).order_by('start_time').\
                        exclude(scheduleoccurrence__occurrenceconfirmation__presence=4).\
                        exclude(scheduleoccurrence__occurrenceconfirmation__presence=5):
                            oc_list.append(x)

                # send email if not empty list for both
                if to and oc_list:
                    title = u"Resumo dos seus eventos para %s, %s.\n\n" % ( week_days[dt.isoweekday()], dt.strftime('%d %b %Y') )

                    # render html email
                    text = Context({'oc_list':oc_list, 'title':title, 'org':org, 'showdt':False})
                    template = get_template("schedule/schedule_notify_careprofessional.html").render(text)
                    # sendmail
                    msg = EmailMessage()
                    msg.content_subtype = 'html'
                    msg.encoding = "utf-8"
                    msg.subject = u"GestorPsi - Resumo diário dos eventos."
                    msg.body = template
                    msg.to = to
                    msg.send()
