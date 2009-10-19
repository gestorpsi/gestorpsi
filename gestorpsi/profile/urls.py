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
from gestorpsi.profile.views import form, save, form_careprofessional, save_careprofessional, change_pass
from gestorpsi.authentication.views import login_check

urlpatterns = patterns('',
    (r'^$', login_check(form)), #profile form
    (r'^careprofessional/$', login_check(form_careprofessional)), #professional profile form
    (r'^save/$', login_check(save)), #save new object
    (r'^save/careprofessional/$', login_check(save_careprofessional)), #save new object
    (r'^chpass/$', login_check(change_pass)), #change password
)
