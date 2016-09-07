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
    This script will to create next invoice, monthly.
    This script will be run every day.
'''

import header

from dateutil.relativedelta import relativedelta
from datetime import date

from gestorpsi.organization.models import Organization 
from gestorpsi.gcm.models.invoice import Invoice

print "# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # "
print "# Invoice - Create new invoice"

# main code
for o in Organization.objects.filter(suspension=False, organization=None):

    # last invoice
    li = Invoice.objects.filter(organization=o).latest('id')

    while li.end_date < date.today()+relativedelta(months=1) and li.start_date < date.today():

        # print to email admin
        print
        print '-- creating a new invoice: %s %s %s' % (o, li.start_date, li.end_date)

        i = Invoice() # new invoice
        i.organization = li.organization
        i.start_date = li.end_date
        i.end_date = li.end_date + relativedelta(months=1)
        i.expiry_date = i.start_date + relativedelta(days=7)
        i.payment_type = li.organization.payment_type
        i.ammount = li.organization.prefered_plan.value
        i.plan = li.organization.prefered_plan
        i.status = 0 # pendente
        i.save()

        li = i # check end_date of new invoice
