#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    script used to create next invoice
    create a new invoice for each organization
'''

import sys
import locale
from os import environ

reload(sys)
sys.setdefaultencoding("utf-8")
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

environ['DJANGO_SETTINGS_MODULE'] = 'gestorpsi.settings'
sys.path.append("/home/redepsi/lib/python2.7")
sys.path.append("/home/redepsi/webapps/gestorpsi_app/git.gestorpsi.com.br")
sys.path.append("/home/redepsi/webapps/gestorpsi_app/git.gestorpsi.com.br/gestorpsi")
sys.path.append("/home/redepsi/webapps/gestorpsi_app/git.gestorpsi.com.br/gestorpsi/gestorpsi")
<<<<<<< HEAD
sys.path.append('..')
=======

from dateutil.relativedelta import relativedelta
from datetime import date, timedelta
>>>>>>> d3b19049f4ff94b496bba590bae493b49e0c7483

from django.core.mail import EmailMessage
from django.core.mail import send_mail

from gestorpsi.settings import URL_HOME, URL_APP, SIGNATURE
from gestorpsi.organization.models import Organization 
from gestorpsi.gcm.models.invoice import Invoice
from gestorpsi.gcm.models.plan import Plan

<<<<<<< HEAD
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')

reload(sys)
sys.setdefaultencoding("utf-8")

# check all invoices that will be expire 10 days from today.
end = date.today() + timedelta(10) # corret
print end
=======
# check all invoices that will be expire 10 days from today.
end = date.today() + timedelta(10) # corret
>>>>>>> d3b19049f4ff94b496bba590bae493b49e0c7483

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# main code
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
for x in Invoice.objects.filter(end_date=end):

    print x

    if not x.organization.suspension: # suspension false

        """
            contratos
                - seram avisados um mes antes de vencer
                - nao gera fatura mensal
            
            boleto 
                termina em um mês ou menos
        """
        i = Invoice() # new invoice
        i.organization = x.organization
        i.start_date = end
        i.end_date = end + relativedelta(months=1)
        i.payment_type = x.organization.payment_type
        i.ammount = x.organization.prefered_plan.value
        i.plan = Plan.objects.get( pk=x.organization.prefered_plan.id )
        i.status = 0 # pendente
        i.save()

        to = [] # send mail to
        # administratror
        for e in x.organization.administrators_():
            if not e.profile.user.email in to:
                to.append(e.profile.user.email) 
        # secretary
        for e in x.organization.secretary_():
            if not e.profile.user.email in to:
                to.append(e.profile.user.email) 

        # send email
        """
            text/body
            1 = url pagamento
            2 = data vencimento assinatura atual
            3 = dia da semana: Segunda-feira
            4 = URL contato
            5 = assinatura gestorPSI
        """
        w = ['segunda-feira','terça-feira','quarta-feira','quinta-feira','sexta-feira','sábado','domingo']
        
<<<<<<< HEAD
        text = u"Bom dia.\n\nSua proxima assinatura já está disponível para pagamento em %s/organization/signature/ Sua assinatura atual vence dia %s, %s, evite ter o seu acesso limitado, pague até esta data.\n\nQualquer dúvida entre em contato pelo link %s/contato/\n" % ( URL_APP , end.strftime("%d %B %Y"), w[date.today().weekday()] , URL_HOME )
        #text = m.encode('utf-8')
        text += u"Quer suspender sua assinatura? Clique aqui %s/organization/suspension/\n\n%s" % ( URL_APP, SIGNATURE )

        msg = EmailMessage()
        msg.subject = u'Assinatura disponível para pagamento - gestorpsi.com.br'
        msg.body = text
        msg.to = to
        msg.send()
=======
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
    bcc = []
    bcc.append('teagom@gmail.com')

    # administratror of org
    for e in x.organization.administrators_():
        if not e.profile.user.email in to:
            to.append(e.profile.user.email) 
    # secretary of org
    for e in x.organization.secretary_():
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
    text = u"Bom dia.\n\nSua próxima assinatura já está disponível para pagamento em %s/organization/signature/\nSua assinatura atual vence dia %s. Evite ter o seu plano suspenso, pague até esta data.\n\nQualquer dúvida entre em contato pelo link %s/contato/\n\n" % ( URL_APP , end.strftime("%d %B %Y, %A") , URL_HOME )
    text += u"Quer suspender sua assinatura? Clique aqui %s/organization/suspension/\n\n%s" % ( URL_APP, SIGNATURE )

    msg = EmailMessage()
    msg.subject = u'Assinatura disponível para pagamento - gestorpsi.com.br'
    msg.body = text
    msg.to = to
    msg.bcc = bcc
    msg.send()
>>>>>>> d3b19049f4ff94b496bba590bae493b49e0c7483
