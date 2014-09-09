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

from django.conf.urls.defaults import patterns, url
from gestorpsi.organization.views import form, save, shortname_is_available, make_second_copy, signature_save, suspension
from gestorpsi.authentication.views import login_check

urlpatterns = patterns('',
    (r'^$', login_check(form)),
    (r'^save/$', login_check(save)),
    (r'^check/(?P<short>.*)/$', (shortname_is_available)),  #check short name
    (r'^second_copy/(?P<invoice>.*)/$', (make_second_copy)),

    url(r'^signature/$', login_check(signature_save), name='organization-signature'),
    url(r'^suspension/$', login_check(suspension), name='organization-suspension'),
)
