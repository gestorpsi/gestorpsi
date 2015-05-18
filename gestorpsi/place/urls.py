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
from gestorpsi.place.views import index, form, save, list,\
    room_form, room_save, room_list, room_index, room_order, place_order
from gestorpsi.authentication.views import login_check

urlpatterns = patterns(
    '',
    # places
    (r'^$', login_check(index)),
    (r'^page(?P<page>(\d)+)/$', login_check(list),
        {'deactive': False}),  # list objects
    (r'^add/$', login_check(form)),
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', login_check(form)),
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/order/$', login_check(place_order)),
    (r'^save/$', login_check(save)),
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/save/$', login_check(save)),
    (r'^initial/(?P<initial>[a-zA-Z])/page(?P<page>(\d)+)/$',
     login_check(list)),  # quick filter
    (r'^filter/(?P<filter>\w+)/page(?P<page>(\d)+)/$',
     login_check(list)),  # quick search
    (r'^filter/(?P<filter>\w+)/$', login_check(list),
     {'no_paging': True}),  # quick search

    # deactivated places
    (r'^initial/(?P<initial>[a-zA-Z])/page(?P<page>(\d)+)/deactive/$',
     login_check(list), {'deactive': True}),  # quick filter
    (r'^initial/(?P<initial>[a-zA-Z])/deactive/$', login_check(list),
     {'deactive': True}),  # quick filter
    (r'^filter/(?P<filter>\w+)/page(?P<page>(\d)+)/deactive/$',
     login_check(list), {'deactive': True}),  # quick search
    (r'^filter/(?P<filter>\w+)/deactive/$', login_check(list),
     {'no_paging': True, 'deactive': True}),  # quick search
    (r'^deactive/$', login_check(index),
     {'deactive': True}),  # list objects deactive
    (r'^page(?P<page>(\d)+)/deactive/$', login_check(list),
     {'deactive': True}),  # list objects

    # rooms
    (r'^room/$', login_check(room_index)),
    (r'^room/add/$', login_check(room_form)),
    (r'^room/(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', login_check(room_form)),
    (r'^room/(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/save/$', login_check(room_save)),
    (r'^room/save/$', login_check(room_save)),
    (r'^room/page(?P<page>(\d)+)$', login_check(room_list)),  # list objects
    (r'^room/(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/order/$', login_check(room_order)),
    (r'^room/initial/(?P<initial>[a-zA-Z])/page(?P<page>(\d)+)/$',
     login_check(room_list)),  # quick filter
    (r'^room/filter/(?P<filter>\w+)/page(?P<page>(\d)+)/$',
     login_check(room_list)),  # quick search
    (r'^room/filter/(?P<filter>\w+)/$', login_check(room_list),
     {'no_paging': True}),  # quick search

    # deactivated rooms
    (r'^room/initial/(?P<initial>[a-zA-Z])/page(?P<page>(\d)+)/deactive/$',
     login_check(room_list), {'deactive': True}),  # quick filter
    (r'^room/initial/(?P<initial>[a-zA-Z])/deactive/$',
     login_check(room_list), {'deactive': True}),  # quick filter
    (r'^room/filter/(?P<filter>\w+)/page(?P<page>(\d)+)/deactive/$',
     login_check(room_list), {'deactive': True}),  # quick search
    (r'^room/filter/(?P<filter>\w+)/deactive/$',
     login_check(room_list),
     {'no_paging': True, 'deactive': True}),  # quick search
    (r'^room/deactive/$', login_check(room_index),
     {'deactive': True}),  # list objects deactive
    (r'^room/page(?P<page>(\d)+)/deactive/$', login_check(room_list),
     {'deactive': True}),  # list objects
)
