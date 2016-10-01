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

from registration.models import RegistrationProfile

from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.contrib.sites.models import get_current_site

from gestorpsi.authentication.models import Profile, Role
from gestorpsi.person.models import Person
from gestorpsi.util.decorators import permission_required_with_403
from gestorpsi.person.views import person_json_list


@permission_required_with_403('users.users_list')
def index(request, deactive=False):
    return render_to_response('users/users_list.html', locals(), context_instance=RequestContext(request))    


@permission_required_with_403('users.users_list')
def list(request, page=1, initial=None, filter=None, deactive=False, permission=False):
    user = request.user

    if deactive:
        object = Profile.objects.filter(org_active=user.get_profile().org_active, user__is_active=False).order_by('user__username')
    else:
        object = Profile.objects.filter(org_active=user.get_profile().org_active, user__is_active=True).order_by('user__username')

    if initial:
        object = object.filter(person__name__istartswith=initial)
        
    if filter:
        object = object.filter(person__name__icontains=filter)

    if permission:
        object = object.filter(user__groups__name=permission)

    return HttpResponse( 
                        simplejson.dumps(person_json_list(request, object, 'users.users_read', page), sort_keys=True),
                        mimetype='application/json'
                        )


@permission_required_with_403('users.users_write')
def set_permission(request, profile, permissions):
    """
        Update group of permission
        profile : Profile()
        permissions : dict of permission group
        return Profile

        Example:
            current (Groups)    A B C D
            Future              A   C
            To exclude            B   D
    """

    if not permissions or not profile:
        return False

    organization = request.user.get_profile().org_active

    # store current permissions
    current = [] # current permission
    for x in profile.user.groups.all():
        current.append(u"%s" % x.name)

    # add permission
    for perm in permissions:

        # check permissions
        if perm in current:
            current.remove(perm) # exclude from current permission, rest will be excluded.

        # Have permisison? Avoid duplicate
        if not Role.objects.filter(profile=profile, organization=organization, group=Group.objects.get(name=perm)):
            # add
            Role.objects.create(profile=profile, organization=organization, group=Group.objects.get(name=perm))

        if not profile.user.groups.filter(name=perm):
            profile.user.groups.add(Group.objects.get(name=perm))

    # Rest of permission in cp will be excluded.
    for perm in current:
        # Are in administrator group?
        if Role.objects.filter(profile=profile, organization=organization, group=Group.objects.get(name=perm)):
            if Role.objects.filter(organization=organization, group=Group.objects.get(name=perm)).distinct().count() < 2:
                messages.error(request, _('Cannot be removed of this permission because is the only one. ( %s )') % perm )
            else:
                Role.objects.filter(profile=profile, organization=organization, group=Group.objects.get(name=perm)).delete()
                profile.user.groups.remove(Group.objects.get(name=perm))

    return profile


@permission_required_with_403('users.users_read')
def form(request, object_id=None):
    """
        Register a new User
        object_id : Person.id
    """
    person = Person.objects.get( pk=object_id, organization=request.user.get_profile().org_active )
    permissions = [] # to check in template, checkbox permissions
    errors = False

    # update
    if hasattr(person,'profile'):
        profile = Profile.objects.get(person=object_id, person__organization=request.user.get_profile().org_active)

        # store permissions
        for x in profile.user.groups.all():
            permissions.append(u"%s" % x.name)

    # save form
    if request.POST:

        permissions = request.POST.getlist('perms')
        username = slugify(request.POST.get('username'))

        if not permissions:
            messages.error(request, _('Select one or more group permission.'))
            errors = True

        if not username:
            messages.error(request, _('Invalid Username'))
            errors = True

        # update
        if hasattr(person,'profile'):
            if not errors:
                profile.user.username = slugify(request.POST.get('username'))
                profile.user.save()
                set_permission(request, profile, permissions)
                messages.success(request, _('User updated successfully'))
                return HttpResponseRedirect('/user/%s/' % person.id)

        # new
        if not hasattr(person,'profile'):
            password = request.POST.get('password')
            pwd_conf = request.POST.get('pwd_conf')
            email = request.POST.get('email_send_user')

            # temp
            user = User()
            user.username = username
            user.password = password # temp
            user.email = email

            profile = Profile()
            profile.user = user

            person.profile = profile

            if User.objects.filter( username=username ):
                messages.error(request, _("Username already exists, try another.") )
                errors = True

            if not password == pwd_conf or not password:
                user.password = ""
                messages.error(request, _('Password confirmation does not match. Please try again') )
                errors = True

            if not email:
                messages.error(request, _('Email address do not match'))
                errors = True

            if not errors:
                site_url = "https://%s" % get_current_site(request).domain

                # overwrite user
                user = RegistrationProfile.objects.create_inactive_user(username, email, password, site_url)
                user.set_password(password)
                user.save()

                profile.user = user
                profile.org_active = request.user.get_profile().org_active
                profile.save()

                person.profile = set_permission(request, profile, permissions)
                person.save()

                # return success to form
                messages.success(request, _('User created successfully. An email will be sent to the user with instructions on how to finish the registration process.'))
                return HttpResponseRedirect('/user/%s/' % person.id)

    # mount form, error, new or update
    return render_to_response('users/users_form.html', {
                        'person': person,
                        'permissions': permissions,
                        }, context_instance=RequestContext(request))


@permission_required_with_403('users.users_write')
def update_pwd(request, obj=False):
    if not obj:
        return HttpResponseRedirect('/')

    # check blank fields
    if not request.POST.get('password_mini') or not request.POST.get('password_mini_conf'):
        messages.error(request, _('All fields are required'))
        return HttpResponseRedirect('/user/%s/' % obj)
        
    # check match fields
    if request.POST.get('password_mini') != request.POST.get('password_mini_conf'):
        messages.error(request, _('Password confirmation does not match. Please try again'))
        return HttpResponseRedirect('/user/%s/' % obj)

    user = Profile.objects.get(person = obj, person__organization=request.user.get_profile().org_active).user
    user.set_password(request.POST.get('password_mini'))
    user.save()
    user.profile.temp = request.POST.get('password_mini')    # temporary field (LDAP)
    user.profile.save()

    messages.success(request, _('Password updated successfully!'))
    return HttpResponseRedirect('/user/%s/' % obj)


@permission_required_with_403('users.users_write')
def set_form_user(request, object_id=0):
    array = {} #json
    
    person = get_object_or_404(Person, pk = object_id, organization=request.user.get_profile().org_active)
    array[0] = slugify(person.name)
    array[1] = u'%s' % person.get_first_email()
    
    return HttpResponse(simplejson.dumps(array), mimetype='application/json')


@permission_required_with_403('users.users_write')
def order(request, profile_id = None):

    object = Profile.objects.get( pk=profile_id, person__organization=request.user.get_profile().org_active )

    if request.user.get_profile() == object:
        messages.error(request, _('Sorry, you can not disable yourself'))
    else:
       # to check if is only one administrator 
        if Role.objects.filter(organization=request.user.get_profile().org_active, group=Group.objects.get(name='administrator')).distinct().count() < 2:
            messages.error(request, _('Cannot be removed of this permission because is the only one. ( %s )') % 'Administrador')
        else:
            if object.user.is_active:
                object.user.is_active = False
            else:
                object.user.is_active = True
                for i in object.user.registrationprofile_set.exclude(activation_key='ALREADY_ACTIVATED'):
                    i.activation_key = 'ALREADY_ACTIVATED'
                    i.save()

            object.user.save()
            messages.success(request, ('%s' % (_('User activated successfully') if object.user.is_active else _('User deactivated successfully'))))
    
    return HttpResponseRedirect('/user/%s/' % object.person.id)


@permission_required_with_403('organization.organization_read')
def username_is_available(request, user):
    """
    Check if username is available:
       0 = No
       1 = Yes
    """
    if User.objects.filter(username__iexact = user).count():
        return HttpResponse("0")
    else:
        return HttpResponse("1")


@permission_required_with_403('users.users_write')
def update_email(request, obj=False):
    # obj format is required by urls.py
    if not obj:
        return HttpResponseRedirect('/user/')
    
    if not request.POST.get('email_mini') == request.POST.get('email_mini_conf') \
            or not request.POST.get('email_mini') \
            or not request.POST.get('email_mini_conf'):

        messages.error(request, _('Email address do not match'))
        return HttpResponseRedirect( '/user/%s/' % obj )
    
    user = Profile.objects.get( person=obj, person__organization=request.user.get_profile().org_active ).user
    
    user.email=request.POST.get('email_mini')
    user.save()

    user.profile.temp = request.POST.get('email_mini')
    user.profile.save()
    
    messages.success(request, _('Email updated successfully!'))
    return HttpResponseRedirect('/user/%s/' % obj)
