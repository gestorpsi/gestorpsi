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
from datetime import date, datetime

from gestorpsi.organization.models import Organization 
from gestorpsi.gcm.models.invoice import Invoice

new_format = datetime(2016, 9, 12,0, 0)

"""
    After or equal 12 09 2016, will use new model, Pay and Use.
    Organization.date_created >= 12 09 2016
"""
print "# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # "
print "# Invoice - Creating invoice new format"

# main code
for o in Organization.objects.filter(suspension=False, organization=None, date_created__gte=new_format):

    inv = [] # invoices to print resume

    # last invoice
    li = Invoice.objects.filter(organization=o).latest('id')

    while li.end_date < date.today()+relativedelta(months=1) and li.start_date < date.today():

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
        inv.append(i)

    # print resume to email admin
    if len(inv) > 0 :
        print '--- Creating a new invoice: %s' % (o)
        for x in inv:
            print '- Start %s End %s Expiry %s' % (x.start_date, x.end_date, x.expiry_date)
        print


"""
    Before 12 09 2016, will use old format, Use and Pay.
    Organization.date_created < 12 09 2016
"""
print "# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # "
print "# Invoice - Creating invoice old format"

# main code
for o in Organization.objects.filter(suspension=False, organization=None, date_created__lt=new_format):

    inv = [] # invoices to print resume

    # last invoice
    li = Invoice.objects.filter(organization=o).latest('id')

    while li.end_date < date.today()+relativedelta(months=1) and li.start_date < date.today():

        i = Invoice() # new invoice
        i.organization = li.organization
        i.start_date = li.end_date
        i.end_date = li.end_date + relativedelta(months=1)
        i.expiry_date = i.end_date
        i.payment_type = li.organization.payment_type
        i.ammount = li.organization.prefered_plan.value
        i.plan = li.organization.prefered_plan
        i.status = 0 # pendente
        i.save()

        li = i # check end_date of new invoice
        inv.append(i)

    # print resume to email admin
    if len(inv) > 0 :
        print '--- Creating a new invoice: %s' % (o)
        for x in inv:
            print '- Start %s End %s Expiry %s' % (x.start_date, x.end_date, x.expiry_date)
        print
