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

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator
from django.conf import settings
from gestorpsi.authentication.models import Profile

def index(request):
    user = request.user
    object = Profile.objects.filter(org_active = user.get_profile().org_active).order_by('user__username')
    paginator = Paginator(object, settings.PAGE_RESULTS)
    object = paginator.page(1)
    return render_to_response('users/users_index.html', {
                                 'object': object,
                                 'paginator': paginator, } ,
                                 context_instance=RequestContext(request))

def list(request, page=1):
    user = request.user
    object = Profile.objects.filter(org_active = user.get_profile().org_active).order_by('user__username')
    paginator = Paginator(object, settings.PAGE_RESULTS)
    object = paginator.page(page)
    return render_to_response('users/users_index.html', {
                                 'object': object,
                                 'paginator': paginator, } ,
                                 context_instance=RequestContext(request))

def form(request, object_id=0):
    object = get_object_or_404(Profile, pk=object_id)

    return render_to_response('users/users_form.html', {
                                'object': object,
                                'emails': ['fdsfd@fsdfds.com','cxvxcvxcvcxvcxvvxc@fsdfds.com'], },
                                context_instance=RequestContext(request))

def save(request, object_id=0):

    try:
        object = get_object_or_404(Client, pk=object_id)
        person = object.person
    except Http404:
        object = Client()
        person = Person()

    object.person = person_save(request, person)
    object.save()

    return HttpResponse(object.id)
