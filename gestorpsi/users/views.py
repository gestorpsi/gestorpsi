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
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User, Group
from registration.models import RegistrationProfile
from gestorpsi.authentication.models import Profile
from gestorpsi.person.models import Person

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
                                'emails': object.person.emails.all(), },
                                context_instance=RequestContext(request))

def form_new_user(request, object_id=''):
    object = Profile()
    object.person = get_object_or_404(Person, pk=object_id)
    object.user = User(username=slugify(object.person.name))
    return render_to_response('users/users_form.html', {
                                'object': object,
                                'emails': object.person.emails.all(), },
                                context_instance=RequestContext(request))

def create_user(request, object_id):
    person = get_object_or_404(Person, pk=object_id)
    organization = request.user.get_profile().org_active
    username = request.POST.get('username')
    password = request.POST.get('password')
    pwd_conf = request.POST.get('pwd_conf')
    email = request.POST.get('email')
    permissions = request.POST.getlist('perms')

    if password == pwd_conf:
        user = RegistrationProfile.objects.create_inactive_user(username, password, email)
        profile = Profile(user=user)
        profile.org_active = organization
        profile.person = person
        profile.save()
        profile.organization.add(organization)

        if permissions.count('administrator'):
            profile.user.groups.add(Group.objects.get(name='administrator'))
        if permissions.count('psychologist'):
            profile.user.groups.add(Group.objects.get(name='psychologist'))
        if permissions.count('secretary'):
            profile.user.groups.add(Group.objects.get(name='secretary'))
        if permissions.count('client'):
            profile.user.groups.add(Group.objects.get(name='client'))

    return HttpResponse("/")

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
