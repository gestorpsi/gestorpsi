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
from gestorpsi.users.views import index, list, form, create_user, update_user, update_pwd, update_email, set_form_user, add, order, username_is_available 
from gestorpsi.authentication.views import login_check

urlpatterns = patterns('',
    (r'^$', login_check(index)),
    (r'^page(?P<page>(\d)+)$', login_check(list)),
    (r'^initial/(?P<initial>[a-zA-Z])/page(?P<page>(\d)+)/$', login_check(list)), # quick filter
    (r'^filter/(?P<filter>[a-zA-Z ]+)/page(?P<page>(\d)+)/$', login_check(list)), # quick search
    (r'^filter/(?P<filter>[a-zA-Z ]+)/$', login_check(list), {'no_paging': True}), # quick search
    #(r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/add/$', login_check(form_new_user)), WILL BE DELETED
    (r'^save/$', login_check(create_user)),
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', login_check(form)),
    (r'^add/$', login_check(add)),
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/save/$', login_check(update_user)),
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/savepwd/$', login_check(update_pwd)),
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/saveemail/$', login_check(update_email)),
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/setformuser/$', login_check(set_form_user)),
    (r'^(?P<profile_id>(\d)+)/order/$', login_check(order)),
    #url(r'^(?P<profile_id>(\d)+)/delete/$', login_check(delete), name='user_delete'),
    (r'^check/(?P<user>.*)/$', login_check(username_is_available)),  #check username
    # DEACTIVE
    (r'^deactive/$', login_check(index), { 'deactive':True }),
    (r'^page(?P<page>(\d)+)/deactive/$', login_check(list), {'deactive':True}),
    (r'^initial/(?P<initial>[a-zA-Z])/page(?P<page>(\d)+)/deactive/$', login_check(list), {'deactive':True} ), # quick filter
    (r'^initial/(?P<initial>[a-zA-Z])/deactive/$', login_check(list), {'deactive':True} ), # quick filter
    (r'^filter/(?P<filter>[a-zA-Z ]+)/page(?P<page>(\d)+)/deactive/$', login_check(list), {'deactive':True} ), # quick search
    (r'^filter/(?P<filter>[a-zA-Z ]+)/deactive/$', login_check(list), {'no_paging': True, 'deactive':True } ), # quick search
)
