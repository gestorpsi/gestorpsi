#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    show last login of user that used GPSI after date
'''

import header
from django.contrib.auth.models import User

checked_list = [] # list of checked organization

for u in User.objects.filter(last_login__gte='2016-10-15', is_staff=False, is_superuser=False):
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
                print 'expiry:%s' % i.expiry_date
                print i.payment_detail
