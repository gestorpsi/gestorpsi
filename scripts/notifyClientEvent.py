#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    this script is used to remember client of next event.
'''

import header
import time

from datetime import date, timedelta, datetime
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.template import Context

from gestorpsi.schedule.models import Occurrence
from django.conf import settings

# check if exist events of next day for all professionals
dt = date.today() + timedelta(settings.NOTIFY_CLIENT_EVENT) # correct

# main code
week_days = (u'Segunda-feira', u'Terça-feira', u'Quarta-feira', u'Quinta-feira', u'Sexta-feira', u'Sábado', u'Domingo')
d = dt.day
m = dt.month
y = dt.year

# send number of mails after pause 
send_pause = 60 # seconds
send_number = 10 # for each 10 emails sent, pause 1 minute
c = 0 # counter

# all occurrence of next day
"""
    to check:
        all events 
            if notify settings is true for this client
                send by email the event of client
"""
for oc in Occurrence.objects.filter(start_time__year=y, start_time__month=m, start_time__day=d): # correct
#for oc in Occurrence.objects.filter(start_time__year=y, start_time__month=m, start_time__day=d, event__referral__organization__id='bcbfdb8e-1641-4478-9e7c-3e0f1befbede'): # develop

    # pause after send a number of emails, avoid smtp close connection, avoid acting like spam
    if c == send_number:
        time.sleep(send_pause)
        print '--- pause %s - %s ' % (c, datetime.today())

    to = [] # list of emails address
    org = oc.event.referral.organization # org

    # to
    for cl in oc.event.referral.client.all():
        if cl.person.notify.filter(org_id=org.id) and cl.person.notify.get(org_id=org.id).client_event: # client set to receive a email to remember the event
            for x in cl.person.emails.all():
                to.append(u'%s' % x.email)

    # send email if not empty list
    if to:
        # render html email
        title = u"Lembrete do atendimento"
        text = Context({'oc':oc, 'title':title, 'org':org})
        template = get_template("schedule/schedule_notify_client_event.html").render(text)
        # sendmail
        msg = EmailMessage()
        msg.content_subtype = 'html'
        msg.encoding = "utf-8"
        msg.subject = u"Lembrete do atendimento com %s." % oc.event.referral.professional.all()[0].person.name
        msg.body = template
        msg.to = to

        try:
            msg.send()
            print '--- sendmail %s ' % oc
        except:
            print '--- sendmail error %s ' % datetime.today()

        c += 1 # if just sendmail
