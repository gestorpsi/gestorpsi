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
from gestorpsi.authentication.views import login_check

from gestorpsi.covenant.views import index, form, list_json

urlpatterns = patterns('',
    url(r'^$', login_check(index), name='covenant-index'), # index list
    url(r'^add/$', login_check(form), name='covenant-add'), # form
    url(r'^(?P<obj>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', login_check(form), name='covenant-edit'), # edit 
    # return json list
    url(r'^list/$', login_check(list_json), name='covenant-list-json'), # return all covenant of organization
    url(r'^list/service/(?P<service>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', login_check(list_json) ), # return all covenant of service
)
