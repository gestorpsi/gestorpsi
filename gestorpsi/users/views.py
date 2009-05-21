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
from django.utils import simplejson
from gestorpsi.util.decorators import permission_required_with_403
from gestorpsi.person.views import person_json_list
from gestorpsi.internet.models import Email, Site, InstantMessenger

@permission_required_with_403('users.users_list')
def index(request):
    person_list = Person.objects.filter(organization = request.user.get_profile().org_active, profile = None)

    return render_to_response('users/users_index.html', {
                                 'person_list': person_list,
                                },
                               context_instance=RequestContext(request))    

@permission_required_with_403('users.users_list')
def list(request, page = 1):
    user = request.user
    object = Profile.objects.filter(org_active = user.get_profile().org_active).order_by('user__username')

    
    return HttpResponse(simplejson.dumps(person_json_list(request, object, 'users.users_read', page)),
                            mimetype='application/json')


@permission_required_with_403('users.users_write')
def form(request, object_id):
    profile = get_object_or_404(Profile, person=object_id)

    # HAVE JUST ONE ADMINISTRATOR?
    show = "False"
    user = request.user
    if ( (Group.objects.get(name='administrator').user_set.all().filter(profile__organization=user.get_profile().org_active).count()) == 1 ):
        if (profile.user.groups.filter(name='administrator').count() == 1 ):
            show = "True"

    groups = [False, False, False, False]   # Template Permission Order: Admin, Psycho, Secretary and Client
    for g in profile.user.groups.all():
        if g.name == "administrator": groups[0] = True
        if g.name == "professional":  groups[1] = True
        if g.name == "secretary":     groups[2] = True
        if g.name == "client":        groups[3] = True
    return render_to_response('users/users_form.html', {
                                'show': show,
                                'profile': profile,
                                'emails': profile.person.emails.all(),
                                'groups': groups, },
                                context_instance=RequestContext(request))

@permission_required_with_403('users.users_read')
def form_new_user(request, object_id):
    profile = Profile()
    profile.person = get_object_or_404(Person, pk=object_id)
    profile.user = User(username=slugify(profile.person.name))
    return render_to_response('users/users_form.html', {
                                'profile': profile,
                                'emails': profile.person.emails.all(), },
                                context_instance=RequestContext(request))

@permission_required_with_403('users.users_write')
def create_user(request):
    person = get_object_or_404(Person, pk=request.POST.get('id_person'))
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
        if permissions.count('professional'):
            profile.user.groups.add(Group.objects.get(name='professional'))
        if permissions.count('secretary'):
            profile.user.groups.add(Group.objects.get(name='secretary'))
        if permissions.count('client'):
            profile.user.groups.add(Group.objects.get(name='client'))
        
        return HttpResponse(profile.person.id)
        
    return HttpResponse('')

@permission_required_with_403('users.users_write')
def update_user(request, object_id):

    user = Profile.objects.get(person = object_id).user

    permissions = request.POST.getlist('perms')

    # DON'T CHANGE PASSWORD IF FIELD IS EMPTY
    if request.POST.get('password') != "":
        user.set_password(request.POST.get('password'))

    # GROUPS
    if permissions.count('administrator'):
        user.groups.add(Group.objects.get(name='administrator'))
    else:
        user.groups.remove(Group.objects.get(name='administrator'))
        
    if permissions.count('professional'):
        user.groups.add(Group.objects.get(name='professional'))
    else:
        user.groups.remove(Group.objects.get(name='professional'))

    if permissions.count('secretary'):
        user.groups.add(Group.objects.get(name='secretary'))
    else:
        user.groups.remove(Group.objects.get(name='secretary'))

    if permissions.count('client'):
        user.groups.add(Group.objects.get(name='client'))
    else:
        user.groups.remove(Group.objects.get(name='client'))

    user.save(force_update = True)

    return HttpResponse(user.profile.id)

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


def update_pwd(request, object_id=0):
   
    user = Profile.objects.get(person = object_id).user
    user.set_password(request.POST.get('password_mini'))

    user.save(force_update = True )

    return HttpResponse(user.profile.id)

def set_form_user(request, object_id=0):
    array = {} #json
   
    try: 
        person = Person.objects.get(pk = object_id)
        array[0] = slugify(person.name)
        array[1] = u'%s' % person.get_first_email()

    except:
        pass
    
    return HttpResponse(simplejson.dumps(array), mimetype='application/json')
