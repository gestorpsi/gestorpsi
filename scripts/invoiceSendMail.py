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
    This script will send email invoice for client
    This script will be run every day.
'''

import header

from datetime import date, timedelta
from django.core.mail import EmailMessage

from gestorpsi.settings import URL_HOME, URL_APP, SIGNATURE, ADMINS_REGISTRATION, invoice_check_expiry
from gestorpsi.gcm.models.invoice import Invoice

def invoice_sendmail():

    # Invoice filter
    invoice_list = [] # list of Invoice

    # check days before expiry
    for d in invoice_check_expiry :
        # check all invoices that will be expire in 10 days.
        expiry = date.today() + timedelta(d) # corret

        print "-- check %s " % expiry
        for i in Invoice.objects.filter(expiry_date=expiry, status=0, organization__suspension=False): # corret code
            if not i in invoice_list:
                invoice_list.append(i)

    # for invoice list
    for li in invoice_list:

        print "-- %s" % ( li )

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
        text_body = u"Bom dia.\n\nSua próxima assinatura já está disponível para pagamento em %s/organization/signature/\nVence em %s, evite ter o seu plano suspenso, pague até esta data.\n\nQualquer dúvida entre em contato pelo link %s/contato/\n" % ( URL_APP , li.expiry_date.strftime("%d %B %Y") , URL_HOME )
        text_body += u"Quer suspender sua assinatura? Clique aqui %s/organization/suspension/\n\n%s" % ( URL_APP, SIGNATURE )

        text_subject = u'Assinatura disponível para pagamento - gestorpsi.com.br'
        bcc = ADMINS_REGISTRATION

        msg = EmailMessage()
        msg.subject = text_subject
        msg.body = text_body
        msg.to = to
        msg.bcc = bcc
        msg.send()


if __name__ == '__main__':
    print "# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # "
    print "# Invoice - Send Mail"
    invoice_sendmail()
