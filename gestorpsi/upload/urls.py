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
from gestorpsi.upload.views import send, attach_form, attach_save
from gestorpsi.referral.models import ReferralAttach, Referral
from django.contrib.auth.decorators import login_required
from gestorpsi.authentication.views import login_check


urlpatterns = patterns('',
    (r'^send/$', login_required(send)), 
    (r'^client/(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/attach/(?P<referral_id>\d+)/$' , login_check(attach_form)),
    (r'^(?P<object_id>\d+)/attach/save/$' , login_check(attach_save))
)
