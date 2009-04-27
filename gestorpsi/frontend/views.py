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

from django.shortcuts import render_to_response
from django.template.context import RequestContext



def index(request):
    #if(request.user.is_authenticated()):
    user = request.user
    return render_to_response('core/main.html', { 
                                'object': user, },
                                context_instance=RequestContext(request))

    #else:        
        #return render_to_response('registration/login.html')

def start(request):
    user = request.user
    return render_to_response('frontend/frontend_start.html', {
                                 'object': user, } ,
                                 context_instance=RequestContext(request))
