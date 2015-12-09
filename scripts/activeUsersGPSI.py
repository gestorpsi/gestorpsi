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
sys.path.append('..')

from django.contrib.auth.models import *

checked_list = [] # list of checked organization

for u in User.objects.filter(last_login__gte='2015-06-01', is_staff=False, is_superuser=False):
    for o in u.profile.person.organization.all():
        if not o in checked_list:

            checked_list.append(o) # add to checked list
            print
            print '----------------- last login:', u.last_login
            print u.username
            print o

            for i in o.invoice_set.all():
                print
                print i.get_status_display(), i.date_payed
                print 'inicio:%s' % i.start_date
                print 'fim:%s' % i.end_date
                print i.payment_detail
