#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    script used to create next invoice
    create a new invoice for each organization
'''

import sys
from os import environ

reload(sys)
sys.setdefaultencoding("utf-8")

environ['DJANGO_SETTINGS_MODULE'] = 'gestorpsi.settings'
sys.path.append('..')

from dateutil.relativedelta import relativedelta
from datetime import date, timedelta

from django.core.mail import EmailMessage
from django.core.mail import send_mail

from gestorpsi.settings import URL_HOME, URL_APP, SIGNATURE
from gestorpsi.organization.models import Organization 
from gestorpsi.gcm.models.invoice import Invoice

# main code
for o in Organization.objects.filter(suspension=False, organization=None):

    # last invoice
    li = Invoice.objects.filter(organization=o).latest('id')

    while li.end_date < date.today()+relativedelta(months=1) and li.start_date < date.today():

        i = Invoice() # new invoice
        i.organization = li.organization
        i.start_date = li.end_date
        i.end_date = li.end_date + relativedelta(months=1)
        i.payment_type = li.organization.payment_type
        i.ammount = li.organization.prefered_plan.value
        i.plan = li.organization.prefered_plan
        i.status = 0 # pendente
        i.save()

        li = i # check end_date of new invoice

        to = [] # send mail to
        # administratror
        for e in li.organization.administrators_():
            if not e.profile.user.email in to:
                to.append(e.profile.user.email) 
        # secretary
        for e in li.organization.secretary_():
            if not e.profile.user.email in to:
                to.append(e.profile.user.email) 

        # send email
        """
            text/body
            1 = url pagamento
            2 = data vencimento assinatura atual
            3 = URL contato
            4 = assinatura gestorPSI
        """
        text = u"Bom dia.\n\nSua próxima assinatura já está disponível para pagamento em %s/organization/signature/ Sua assinatura atual vence dia %s, evite ter o seu plano suspenso, pague até esta data.\n\nQualquer dúvida entre em contato pelo link %s/contato/\n\n" % ( URL_APP , li.end_date.strftime("%d %B %Y, %A") , URL_HOME )
        text += u"Quer suspender sua assinatura? Clique aqui %s/organization/suspension/\n\n%s" % ( URL_APP, SIGNATURE )

        msg = EmailMessage()
        msg.subject = u'Assinatura disponível para pagamento - gestorpsi.com.br'
        msg.body = text
        msg.to = to
        msg.send()
