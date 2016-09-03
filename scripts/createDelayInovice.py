#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    This script will to create next invoice, monthly.
    This script will be run every day.
'''

import header

from dateutil.relativedelta import relativedelta
from datetime import date

from django.core.mail import EmailMessage

from gestorpsi.settings import URL_HOME, URL_APP, SIGNATURE
from gestorpsi.organization.models import Organization 
from gestorpsi.gcm.models.invoice import Invoice

# main code
for o in Organization.objects.filter(suspension=False, organization=None):

    # last invoice
    li = Invoice.objects.filter(organization=o).latest('id')

    while li.end_date < date.today()+relativedelta(months=1) and li.start_date < date.today():

        # print to email admin
        print 'Creating new invoice: %s %s %s' % (o, li.start_date, li.end_date)
        print

        i = Invoice() # new invoice
        i.organization = li.organization
        i.start_date = li.end_date
        i.end_date = li.end_date + relativedelta(months=1)
        i.expiry_date = li.start_date + relativedelta(days=7)
        i.payment_type = li.organization.payment_type
        i.ammount = li.organization.prefered_plan.value
        i.plan = li.organization.prefered_plan
        i.status = 0 # pendente
        i.save()

        li = i # check end_date of new invoice

        to = [] # send mail to
        # administratror
        for e in li.organization.administrators_():
            if e.profile.user.is_active and not e.profile.user.email in to:
                to.append(e.profile.user.email) 
        # secretary
        for e in li.organization.secretary_():
            if e.profile.user.is_active and not e.profile.user.email in to:
                to.append(e.profile.user.email) 

        # send email
        """
            text/body order s% of python
            1 = url pagamento
            2 = data vencimento assinatura atual
            3 = URL contato
            4 = assinatura gestorPSI
        """
        text_body = u"Bom dia.\n\nSua próxima assinatura já está disponível para pagamento em %s/organization/signature/ Sua assinatura atual vence dia %s, evite ter o seu plano suspenso, pague até esta data.\n\nQualquer dúvida entre em contato pelo link %s/contato/\n\n" % ( URL_APP , li.end_date.strftime("%d %B %Y, %A") , URL_HOME )
        text_body += u"Quer suspender sua assinatura? Clique aqui %s/organization/suspension/\n\n%s" % ( URL_APP, SIGNATURE )

        text_subject = u'Assinatura disponível para pagamento - gestorpsi.com.br'
        bcc = ADMINS_REGISTRATION

        msg = EmailMessage()
        msg.subject = text_subject
        msg.body = text_body
        msg.to = to
        msg.bcc = bcc
        msg.send()
