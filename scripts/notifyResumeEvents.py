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
day = date.today() + timedelta(1) # corret
day = date.today() + timedelta(0) # test

# main code
d = date.today().day
m = date.today().month
y = date.today().year

# find events of next day
for o in Occurrence.objects.filter(start_time__year=y, start_time__month=m, start_time__day=d):
    
    """
        profissional quer receber o resumo do dia?
    """
    for p in o.event.referral.professional.all():

        events = []
        to = []

        if p.person.notify.all()[0].resume_daily_event:
            for x in p.person.emails.all():
                to.append(x)
            for x in Occurrence.objects.filter(start_time__year=y, start_time__month=m, start_time__day=d, event__referral__professional=c).order_by('-start_time'):
                events.append(x)
               
            #'''
                #send mail just to user is_active = True
            #'''
            ## administratror of org
            #for e in x.organization.administrators_():
                #if e.profile.user.is_active and not e.profile.user.email in to:
                    #to.append(e.profile.user.email) 

            ## secretary of org
            #for e in x.organization.secretary_():
                #if e.profile.user.is_active and not e.profile.user.email in to:
                    #to.append(e.profile.user.email) 

            # send email
            """
                text/body
                1 = url pagamento
                2 = data vencimento assinatura atual
                3 = URL contato
                4 = assinatura gestorPSI
            """
            text = u"Bom dia.\n\nSua próxima assinatura já está disponível para pagamento em %s/organization/signature/\nSua assinatura atual vence dia %s. Evite ter o seu plano suspenso, pague até esta data.\n\nQualquer dúvida entre em contato pelo link %s/contato/\n\n" % ( URL_APP , end.strftime("%d %B %Y, %A") , URL_HOME )
            text += u"Quer suspender sua assinatura? Clique aqui %s/organization/suspension/\n\n%s" % ( URL_APP, SIGNATURE )

            msg = EmailMessage()
            msg.subject = u'GestorPsi - Resumo dos eventos'
            msg.body = text
            msg.to = to
            msg.bcc = bcc
            msg.send()
