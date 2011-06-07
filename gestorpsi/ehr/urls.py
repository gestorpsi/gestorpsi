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

from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from gestorpsi.authentication.views import login_check
from gestorpsi.ehr.views import *

urlpatterns = patterns('',
    # Session's URL
    (r'^(?P<client_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/(?P<referral_id>\d+)/session/$', login_check(session_list)),
    (r'^(?P<client_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/(?P<referral_id>\d+)/session/(?P<session_id>\d+)/item/$', login_check(session_item_html)),
    (r'^(?P<client_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/(?P<referral_id>\d+)/session/add/$', login_check(session_form)),
    (r'^(?P<client_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/(?P<referral_id>\d+)/session/(?P<session_id>\d+)/$', login_check(session_form)),

    # Diagnosis's URL
    (r'^(?P<client_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/(?P<referral_id>\d+)/diagnosis/$', login_check(diagnosis_list)),
    (r'^(?P<client_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/(?P<referral_id>\d+)/diagnosis/(?P<diagnosis_id>\d+)/item/$', login_check(diagnosis_item_html)),
    (r'^(?P<client_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/(?P<referral_id>\d+)/diagnosis/add/$', login_check(diagnosis_form)),
    (r'^(?P<client_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/(?P<referral_id>\d+)/diagnosis/(?P<diagnosis_id>\d+)/$', login_check(diagnosis_form)),
    
    # Demand's URL
    (r'^(?P<client_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/(?P<referral_id>\d+)/demand/$', login_check(demand_list)),
    (r'^(?P<client_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/(?P<referral_id>\d+)/demand/(?P<demand_id>\d+)/item/$', login_check(demand_item_html)),
    (r'^(?P<client_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/(?P<referral_id>\d+)/demand/add/$', login_check(demand_form)),
    (r'^(?P<client_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/(?P<referral_id>\d+)/demand/(?P<demand_id>\d+)/$', login_check(demand_form)),
)
