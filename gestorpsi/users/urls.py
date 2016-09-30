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
from gestorpsi.users.views import index, list, form, update_pwd, order, username_is_available, update_email
from gestorpsi.authentication.views import login_check

urlpatterns = patterns('',
    url(r'^$', login_check(index), name='user-index'),
    # search
    (r'^page(?P<page>(\d)+)$', login_check(list)),
    (r'^page(?P<page>(\d)+)/permission/(?P<permission>[a-z]+)/$', login_check(list)), # filter permission
    (r'^initial/(?P<initial>[a-zA-Z])/page(?P<page>(\d)+)/$', login_check(list)), # quick filter
    (r'^initial/(?P<initial>[a-zA-Z])/permission/(?P<permission>[a-z]+)/page(?P<page>(\d)+)/$', login_check(list)), # quick filter
    (r'^filter/(?P<filter>[a-zA-Z ]+)/page(?P<page>(\d)+)/$', login_check(list)), # quick search
    (r'^filter/(?P<filter>[a-zA-Z ]+)/permission/(?P<permission>[a-z]+)/page(?P<page>(\d)+)/$', login_check(list)), # quick search and permission
    # form
    (r'^check/(?P<user>.*)/$', login_check(username_is_available)), # check if username are available
    url(r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', login_check(form), name='user-form'), # mount form and save
    url(r'^(?P<obj>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/saveemail/$', login_check(update_email), name="user-form-email"),
    url(r'^(?P<obj>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/savepwd/$', login_check(update_pwd), name='user-form-password'),
    # deactive or active
    url(r'^(?P<profile_id>(\d)+)/order/$', login_check(order), name='user-form-order'),
    # deactive
    url(r'^deactive/$', login_check(index), { 'deactive':True }, name='user-index-deactive'),
    (r'^page(?P<page>(\d)+)/deactive/$', login_check(list), {'deactive':True}),
    (r'^page(?P<page>(\d)+)/permission/(?P<permission>[a-z]+)/deactive/$', login_check(list), {'deactive':True}), # filter permission
    (r'^initial/(?P<initial>[a-zA-Z])/deactive/$', login_check(list), {'deactive':True} ), # quick filter
    (r'^initial/(?P<initial>[a-zA-Z])/page(?P<page>(\d)+)/deactive/$', login_check(list), {'deactive':True} ), # quick filter
    (r'^initial/(?P<initial>[a-zA-Z])/permission/(?P<permission>[a-z]+)/page(?P<page>(\d)+)/deactive/$', login_check(list), {'deactive':True} ), # quick filter
    (r'^filter/(?P<filter>[a-zA-Z ]+)/page(?P<page>(\d)+)/deactive/$', login_check(list), {'deactive':True} ), # quick search
    (r'^filter/(?P<filter>[a-zA-Z ]+)/deactive/$', login_check(list), {'no_paging': True, 'deactive':True } ), # quick search
)
