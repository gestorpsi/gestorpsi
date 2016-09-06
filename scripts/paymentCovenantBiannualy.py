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
    script to create receive weekly, every sunday night.
    create a new receive for each covenant of referral
'''

import header

from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.db.models.loading import get_models
loaded_models = get_models()

from gestorpsi.financial.models import Receive
from gestorpsi.referral.models import Referral

'''
    Covenant.charge = 14 : biannualy
    Referral.date : date join referral service

    filter by:
    (today - 6Monthly) = referral.date
'''
covenant_charge = 14

# today - 6 months
year = (datetime.today()-relativedelta(months=6)).year
month = (datetime.today()-relativedelta(months=6)).month
day = (datetime.today()-relativedelta(months=6)).day

# main code
for r in Referral.objects.filter(covenant__isnull=False, covenant__charge=covenant_charge, referraldischarge__isnull=True, date__year=year, date__month=month, date__day=day):

    '''
        filter for all referall that don't have discharge
    '''
    
    # create a receive for each covenant of referral
    for c in r.covenant.filter(charge=covenant_charge):

        # new
        receive = Receive()
        receive.created = datetime
        receive.name = c.name
        receive.price = c.price
        receive.off = 0
        receive.total = c.price
        receive.covenant_charge = c.charge
        receive.covenant_id = c.id

        # clear all
        receive.covenant_payment_way_options = ''
        for pw in c.payment_way.all():
            x = "(%s,'%s')," % ( pw.id , pw.name ) # need be a dict
            receive.covenant_payment_way_options += x

        # add referral
        receive.referral = r

        # save
        receive.save()
