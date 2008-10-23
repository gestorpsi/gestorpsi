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

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.utils.translation import gettext as _
from gestorpsi.authentication.models import CustomUser
from gestorpsi.organization.models import Organization


def index(request):
    if(request.user.is_authenticated()):
        return render_to_response('core/main.html')
    else:        
        return render_to_response('registration/login.html')
    
