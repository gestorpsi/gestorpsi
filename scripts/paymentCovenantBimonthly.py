#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    script to create payment weekly, every sunday night.
    create a new payment for each covenant of referral
'''

import header

from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.db.models.loading import get_models
loaded_models = get_models()

from gestorpsi.financial.models import Payment
from gestorpsi.referral.models import Referral

'''
    Covenant.charge = 13 : bimonthly
    Referral.date : date join referral service

    filter by:
    (today - 2Monthly) = referral.date
'''
covenant_charge = 13

# today - 2 months
year = (datetime.today()-relativedelta(months=2)).year
month = (datetime.today()-relativedelta(months=2)).month
day = (datetime.today()-relativedelta(months=2)).day

# main code
for r in Referral.objects.filter(covenant__isnull=False, covenant__charge=covenant_charge, referraldischarge__isnull=True, date__year=year, date__month=month, date__day=day):

    '''
        filter for all referall that don't have discharge
    '''
    
    # create a payment for each covenant of referral
    for c in r.covenant.filter(charge=covenant_charge):

        # new
        payment = Payment()
        payment.created = datetime
        payment.name = c.name
        payment.price = c.price
        payment.off = 0
        payment.total = c.price
        payment.covenant_charge = c.charge

        # clear all
        payment.covenant_payment_way_options = ''
        for pw in c.payment_way.all():
            x = "(%s,'%s')," % ( pw.id , pw.name ) # need be a dict
            payment.covenant_payment_way_options += x

        # add referral
        payment.referral = r

        # save
        payment.save()
