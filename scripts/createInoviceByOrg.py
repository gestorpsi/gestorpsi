#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from os import environ

from dateutil.relativedelta import relativedelta
from datetime import date

environ['DJANGO_SETTINGS_MODULE'] = 'gestorpsi.settings'
sys.path.append('..')

from gestorpsi.organization.models import Organization 
from gestorpsi.gcm.models.payment import PaymentType
from gestorpsi.gcm.models.invoice import Invoice
from gestorpsi.gcm.models.plan import Plan

# main code
for o in Organization.objects.filter(suspension=False, organization=None):

    # when client do register a automatic invoice will be created.
    # Org have no less than one invoice by default roles system invoice.
    try:
        last = Invoice.objects.filter(organization=o).latest('end_date')
    except:
        last = Invoice()
        last.start_date = date.today() - relativedelta(months=1)
        last.end_date = date.today()

    # can not be None
    if o.payment_type == None:
        o.payment_type = PaymentType.objects.get(pk=1) # credit card
        o.save()

    # can not be None
    if o.prefered_plan == None:
        o.prefered_plan = Plan.objects.get(pk=2) # 1 professional
        o.save()

    """
        contratos
            - seram avisados um mes antes de vencer
            - nao gera fatura mensal
        
        boleto 
            termina em um mês ou menos
    """
    if last.end_date <= ( date.today() + relativedelta(months=1) ):
        i = Invoice() # new invoice
        i.organization = o
        i.start_date = last.end_date
        i.end_date = i.start_date + relativedelta(months=1)
        i.payment_type = o.payment_type
        i.ammount = o.prefered_plan.value
        i.plan = o.prefered_plan
        i.status = 0 # pendente
        i.save()
