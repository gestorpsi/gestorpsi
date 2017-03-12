#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    script used to send email for professional
    resume of events of next day
'''

import sys
import locale
from os import environ

reload(sys)
sys.setdefaultencoding("utf-8")
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

environ['DJANGO_SETTINGS_MODULE'] = 'gestorpsi.settings'
sys.path.append('..')

from dateutil.relativedelta import relativedelta
from datetime import date, timedelta

from django.core.mail import EmailMessage
from django.core.mail import send_mail

from gestorpsi.settings import URL_HOME, URL_APP, SIGNATURE
from gestorpsi.organization.models import Organization 
from gestorpsi.gcm.models.invoice import Invoice

from gestorpsi.schedule.models import *

# check if has events of next day for all professional
dt = date.today() + timedelta(1) # correct
dt = date.today() - timedelta(5) # test

# main code
d = dt.day
m = dt.month
y = dt.year

# sent professional list
sent = []

# find events of next day
#for o in Occurrence.objects.filter(start_time__year=y, start_time__month=m, start_time__day=d): # correct
for o in Occurrence.objects.filter(start_time__year=y, start_time__month=m, start_time__day=d, event__referral__organization__id='bcbfdb8e-1641-4478-9e7c-3e0f1befbede'): # test
    """
        profissional quer receber o resumo do dia?
    """
    for p in o.event.referral.professional.all():
        events = []
        to = []

        if p.person.notify.all() and p.person.notify.all()[0].resume_daily_event and p not in sent:
            sent.append(p) # add professional

            for x in p.person.emails.all():
                to.append(u'%s' % x.email)

            # send email
            if to:
                text = "GestorPsi - Resumo dos eventos para o dia %s\n\n" % dt
                # render occurrence
                for x in Occurrence.objects.filter(start_time__year=y, start_time__month=m, start_time__day=d, event__referral__professional=p).order_by('-start_time'):
                    text += "%s - %s\n" % (x.start_time, x)
               
                """
                    text/body
                    1 = url pagamento
                    2 = data vencimento assinatura atual
                    3 = URL contato
                    4 = assinatura gestorPSI
                """
                #text = u"Bom dia.\n\nSua próxima assinatura já está disponível para pagamento em %s/organization/signature/\nSua assinatura atual vence dia %s. Evite ter o seu plano suspenso, pague até esta data.\n\nQualquer dúvida entre em contato pelo link %s/contato/\n\n" % ( URL_APP , end.strftime("%d %B %Y, %A") , URL_HOME )
                #text += u"Quer suspender sua assinatura? Clique aqui %s/organization/suspension/\n\n%s" % ( URL_APP, SIGNATURE )
                msg = EmailMessage()
                msg.to = to
                msg.body = text
                msg.subject = u'GestorPsi - Resumo dos eventos'
                print '---- SENDMAIL '
                msg.send()
