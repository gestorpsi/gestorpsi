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

import datetime
from django.http import Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from gestorpsi.client.models import Client

def start(request):
    profile = request.user.get_profile()
    date = datetime.datetime.now()
    
    """ users client home page """
    if request.user.get_profile().person.is_client():
        object = Client.objects.get(pk=request.user.get_profile().person.client.id)
        return render_to_response('frontend/frontend_client_start.html', locals(), context_instance=RequestContext(request))
    
    """ users admistrator home page """
    if request.user.get_profile().person.is_careprofessional() or request.user.get_profile().person.is_administrator():
        return render_to_response('frontend/frontend_start.html', locals(), context_instance=RequestContext(request))
    
    raise Http404
