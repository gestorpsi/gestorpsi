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
    script used to create monthly invoice
    create a new invoice for each organization
'''

import header

from dateutil.relativedelta import relativedelta
from datetime import date, timedelta

from django.core.mail import EmailMessage

from django.conf import settings
from gestorpsi.gcm.models.invoice import Invoice

# check all invoices that will be expire 10 days from today.
end = date.today() + timedelta(10) # corret

# main code

# Create next invoice if last was paid and organization is not suspension
for x in Invoice.objects.filter(end_date=end, status__gt=0, organization__suspension=False):
    """
        contratos
            - seram avisados um mes antes de vencer
            - nao gera fatura mensal
        
        boleto 
            termina em um mês ou menos
    """
    # non exist
    if Invoice.objects.filter( end_date=end+relativedelta(months=1), organization=x.organization ).count() == 0 :

        i = Invoice() # new invoice
        i.organization = x.organization
        i.start_date = end
        i.end_date = end + relativedelta(months=1)
        i.payment_type = x.organization.payment_type
        i.ammount = x.organization.prefered_plan.value
        i.plan = x.organization.prefered_plan
        i.status = 0 # pendente
        i.save()

    to = [] # send mail to

    '''
        send mail just to user is_active = True
    '''
    # administratror of org
    for e in x.organization.administrators_():
        if e.profile.user.is_active and not e.profile.user.email in to:
            to.append(e.profile.user.email) 

    # secretary of org
    for e in x.organization.secretary_():
        if e.profile.user.is_active and not e.profile.user.email in to:
            to.append(e.profile.user.email) 

    # send email
    """
        text/body
        1 = url pagamento
        2 = data vencimento assinatura atual
        3 = URL contato
        4 = assinatura gestorPSI
    """
    text = u"Bom dia.\n\nSua próxima assinatura já está disponível para pagamento em %s/organization/signature/\nSua assinatura atual vence dia %s. Evite ter o seu plano suspenso, pague até esta data.\n\nQualquer dúvida entre em contato pelo link %s/contato/\n\n" % ( settings.URL_APP , end.strftime("%d %B %Y, %A") , settings.URL_HOME )
    text += u"Quer suspender sua assinatura? Clique aqui %s/organization/suspension/\n\n%s" % ( settings.URL_APP, settings.SIGNATURE )

    msg = EmailMessage()
    msg.subject = u'Assinatura disponível para pagamento - gestorpsi.com.br'
    msg.body = text
    msg.to = to
    msg.bcc = settings.ADMINS_REGISTRATION
    msg.send()
