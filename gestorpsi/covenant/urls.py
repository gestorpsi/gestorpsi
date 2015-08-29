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

from gestorpsi.covenant.views import index, form, list_filter, list_json, order

urlpatterns = patterns('',
    url(r'^$', login_check(index), name='covenant-index'), # index, active list
    url(r'^deactive/$', login_check(index), {'active':False}, name='covenant-list-deactive'), # deactive list
    url(r'^add/$', login_check(form), name='covenant-add'), # add
    url(r'^(?P<obj>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', login_check(form), name='covenant-edit'), # edit 
    # list
    url(r'^list/active/$', login_check(list_filter)), # return all ACTIVE covenant of organization
    url(r'^list/deactive/$', login_check(list_filter), {'active':False}), # return all DEACTIVE covenant of organization
    # quick search
    url(r'^list/active/(?P<filter>\w+)/$', login_check(list_filter)), # search method get
    url(r'^list/deactive/(?P<filter>\w+)/$', login_check(list_filter)), # search method get
    # active or deactive
    url(r'^(?P<obj>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/order/$', login_check(order), name='covenant-order' ), # return all covenant of service

    # json
    # referral form client
    url(r'^list/service/(?P<service>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', login_check(list_json) ), # return all covenant of service
    # get informations of covenant
    url(r'^(?P<obj>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/get/$', login_check(list_json) ), # return all covenant of service
    # return all covenants
    url(r'^list/all/$', login_check(list_json), { 'order':'all'} ),
    # return all covenants for groups
    url(r'^list/group/$', login_check(list_json), { 'order':'group'} ),
)
