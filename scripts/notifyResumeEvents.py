#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    script used to send the resume of events of day for professional
'''

import header

from datetime import date, timedelta
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.template import Context

from gestorpsi.schedule.models import Occurrence

# check if exist events of next day for all professionals
dt = date.today() + timedelta(1) # correct

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
for oc in Occurrence.objects.filter(start_time__year=y, start_time__month=m, start_time__day=d): # correct
#for oc in Occurrence.objects.filter(start_time__year=y, start_time__month=m, start_time__day=d, event__referral__organization__id='bcbfdb8e-1641-4478-9e7c-3e0f1befbede'): # debug/test
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

                # list of occurrence of professional in day
                for x in Occurrence.objects.filter(start_time__year=y, start_time__month=m, start_time__day=d,\
                        event__referral__professional=pr, event__referral__organization=org).order_by('start_time'):
                    oc_list.append(x)

                # send email if not empty list for both
                if to and oc_list:
                    title = u"Resumo dos seus eventos para %s, %s.\n\n" % ( week_days[date.today().isoweekday()], dt.strftime('%d %b %Y') )

                    # render html email
                    text = Context({'oc_list':oc_list, 'title':title, 'org':org})
                    template = get_template("schedule/schedule_notify_careprofessional.html").render(text)
                    # sendmail
                    msg = EmailMessage()
                    msg.content_subtype = 'html'
                    msg.encoding = "utf-8"
                    msg.subject = u"GestorPsi - Resumo diário dos eventos."
                    msg.body = template
                    msg.to = to
                    msg.send()
