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
from gestorpsi.socioeconomic.views import socioeconomic_home, socioeconomic_transportation, socioeconomic_transportation_save
from gestorpsi.authentication.views import login_check

urlpatterns = patterns('',
    (r'^$', login_check(index)), #list objects
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/socioeconomic/$', login_check(socioeconomic_home)),
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/socioeconomic/transportation/$', login_check(socioeconomic_transportation)),
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/socioeconomic/transportation/(?P<transportation_id>(\d)+)/$', login_check(socioeconomic_transportation)),
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/socioeconomic/transportation/save/$', login_check(socioeconomic_transportation_save)),
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/socioeconomic/transportation/save/(?P<transportation_id>(\d)+)/$', login_check(socioeconomic_transportation_save)),
)
