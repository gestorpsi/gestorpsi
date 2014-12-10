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

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.contrib.sites.models import get_current_site
# import registration
from registration.models import RegistrationProfile
from gestorpsi.authentication.models import Profile, Role
from gestorpsi.person.models import Person
from django.utils import simplejson
from gestorpsi.util.decorators import permission_required_with_403
from gestorpsi.person.views import person_json_list

permission_required_with_403('users.users_list')


def index(request, deactive=False):
    return render_to_response(
        'users/users_list.html',
        locals(),
        context_instance=RequestContext(request)
        )


@permission_required_with_403('users.users_list')
def list(request, page=1, initial=None, filter=None, deactive=False):
    user = request.user

    if deactive:
        object = Profile.objects.filter(
            org_active=user.get_profile().org_active,
            user__is_active=False).order_by('user__username')
    else:
        object = Profile.objects.filter(
            org_active=user.get_profile().org_active,
            user__is_active=True).order_by('user__username')

    if initial:
        object = object.filter(person__name__istartswith=initial)

    if filter:
        object = object.filter(person__name__icontains=filter)

    return HttpResponse(
        simplejson.dumps(
            person_json_list(
                request,
                object,
                'users.users_read',
                page),
            sort_keys=True),
        mimetype='application/json')


@permission_required_with_403('users.users_read')
def form(request, object_id=None):
    user = request.user
    try:
        profile = Profile.objects.get(
            person=object_id,
            person__organization=request.user.get_profile().org_active)
        # have just one administrator?
        show = "False"

        if ((Group.objects.get(
                name='administrator').user_set.all().filter(
                    profile__organization=user.get_profile().org_active
                    ).count()) == 1):
            if (profile.user.groups.filter(name='administrator').count() == 1):
                show = "True"

        # Template Permission Order:Admin,Psycho, Secretary, Client and Student
        groups = [False, False, False, False, False]
        for g in profile.user.groups.all():
            if g.name == "administrator":
                groups[0] = True
            if g.name == "professional":
                groups[1] = True
            if g.name == "secretary":
                groups[2] = True
            if g.name == "client":
                groups[3] = True
            if g.name == "student":
                groups[4] = True
        return render_to_response(
            'users/users_form.html', {
                'show': show,
                'profile': profile,
                'person': profile.person,
                'emails': profile.person.emails.all(),
                'groups': groups,
                },
            context_instance=RequestContext(request)
            )
    except:
        return render_to_response('users/users_form.html', {
            'person_list': Person.objects.filter(
                pk=object_id,
                organization=request.user.get_profile().org_active,
                profile=None),
            'person': Person.objects.get(
                pk=object_id,
                organization=request.user.get_profile().org_active),
            'clss': request.GET.get('clss'),
            }, context_instance=RequestContext(request))


@permission_required_with_403('users.users_read')
def add(request):
    return render_to_response(
        'users/users_form.html', {
            'person_list': Person.objects.filter(
                organization=request.user.get_profile().org_active,
                profile=None),
            'clss': request.GET.get('clss'),
            },
        context_instance=RequestContext(request))


@permission_required_with_403('users.users_write')
def create_user(request):
    if not request.method == 'POST':
        raise Http404

    if User.objects.filter(username=request.POST.get('username').strip().lower()):
        messages.success(
            request,
            _('Error adding user <b>%s</b>: Username already exists.')
            % request.POST.get('username').strip().lower())
        return HttpResponseRedirect('/user/add/?clss=error')

    person = get_object_or_404(
        Person,
        pk=request.POST.get('id_person'),
        organization=request.user.get_profile().org_active
        )
    organization = request.user.get_profile().org_active
    username = request.POST.get('username').strip().lower()
    password = request.POST.get('password')
    pwd_conf = request.POST.get('pwd_conf')
    email = request.POST.get('email_send_user')
    permissions = request.POST.getlist('perms')

    if not password == pwd_conf:
        messages.success(request, _('Error: Supplied passwords are differents.'))
        return HttpResponseRedirect('/user/add/?clss=error')

    site_url = "http://%s" % get_current_site(request).domain if not request.is_secure else "http://%s" % get_current_site(request).domain
    user = RegistrationProfile.objects.create_inactive_user(
        username,
        email,
        password,
        site_url
        )

    # this is required! without it, password will not set ok
    user.set_password(password)
    user.save(force_update=True)

    profile = Profile(user=user)
    profile.org_active = organization
    profile.temp = password    # temporary field (LDAP)
    profile.person = person
    profile.save()
    # profile.organization.add(organization)

    if permissions.count('administrator'):
        Role.objects.create(
            profile=profile,
            organization=organization,
            group=Group.objects.get(name='administrator')
            )
        profile.user.groups.add(Group.objects.get(name='administrator'))

    if permissions.count('professional'):
        Role.objects.create(
            profile=profile,
            organization=organization,
            group=Group.objects.get(name='professional')
            )
        profile.user.groups.add(Group.objects.get(name='professional'))

    if permissions.count('secretary'):
        Role.objects.create(
            profile=profile,
            organization=organization,
            group=Group.objects.get(name='secretary')
            )
        profile.user.groups.add(Group.objects.get(name='secretary'))

    if permissions.count('client'):
        Role.objects.create(
            profile=profile,
            organization=organization,
            group=Group.objects.get(name='client')
            )
        profile.user.groups.add(Group.objects.get(name='client'))

    if permissions.count('student'):
        Role.objects.create(
            profile=profile,
            organization=organization,
            group=Group.objects.get(name='student')
            )
        profile.user.groups.add(Group.objects.get(name='student'))

    messages.success(request, _('User created successfully. An email will be sent to the user with instructions on how to finish the registration process.'))

    return HttpResponseRedirect('/user/%s/' % profile.person.id)


@permission_required_with_403('users.users_write')
def update_user(request, object_id):
    organization = request.user.get_profile().org_active
    profile = Profile.objects.get(
        person=object_id,
        person__organization=request.user.get_profile().org_active
        )
    permissions = request.POST.getlist('perms')

    # groups - clear all permissions and re-create them
    profile.user.groups.clear()
    Role.objects.filter(organization=organization, profile=profile).delete()

    if permissions.count('administrator'):
        Role.objects.create(
            profile=profile,
            organization=organization,
            group=Group.objects.get(name='administrator')
            )
        profile.user.groups.add(Group.objects.get(name='administrator'))

    if permissions.count('professional'):
        Role.objects.create(
            profile=profile,
            organization=organization,
            group=Group.objects.get(name='professional')
            )
        profile.user.groups.add(Group.objects.get(name='professional'))

    if permissions.count('secretary'):
        Role.objects.create(
            profile=profile,
            organization=organization,
            group=Group.objects.get(name='secretary')
            )
        profile.user.groups.add(Group.objects.get(name='secretary'))

    if permissions.count('client'):
        Role.objects.create(
            profile=profile,
            organization=organization,
            group=Group.objects.get(name='client')
            )
        profile.user.groups.add(Group.objects.get(name='client'))

    if permissions.count('student'):
        Role.objects.create(
            profile=profile,
            organization=organization,
            group=Group.objects.get(name='student')
            )
        profile.user.groups.add(Group.objects.get(name='student'))

    profile.user.save(force_update=True)

    messages.success(request, _('User updated successfully'))

    return HttpResponseRedirect('/user/%s/' % profile.person.id)


def verify_requests(actual_password, request, request_confirmation):
    if not actual_password:
        return "Actual Password required."
    if not request or not request_confirmation:
        return "All fields are required"
    if request != request_confirmation:
        return "Confirmation does not match. Please try again"

    return ""


@permission_required_with_403('users.users_write')
def update_pwd(request, object_id=0):
    invalid_passwords = verify_requests(
        request.POST.get('actual_password_mini'),
        request.POST.get('password_mini'),
        request.POST.get('password_mini_conf')
        )

    if invalid_passwords != "":
        messages.error(request, _(invalid_passwords))
        return HttpResponseRedirect('/user/%s/' % object_id)

    user = Profile.objects.get(
        person=object_id,
        person__organization=request.user.get_profile().org_active).user
    if not user.check_password(request.POST.get('actual_password_mini')):
        messages.error(request, _('Password Incorrect'))
        return HttpResponseRedirect('/user/%s/' % object_id)

    user.set_password(request.POST.get('password_mini'))
    # temporary field (LDAP)
    user.profile.temp = request.POST.get('password_mini')
    user.profile.save()
    user.save(force_update=True)

    messages.success(request, _('Password updated successfully!'))
    return HttpResponseRedirect('/user/%s/' % object_id)


@permission_required_with_403('users.users_write')
def update_email(request, object_id=0):
    invalid_emails = verify_requests(
        request.POST.get('actual_password_mini'),
        request.POST.get('email_mini'),
        request.POST.get('email_mini_conf')
        )

    if invalid_emails != "":
        messages.error(request, _(invalid_emails))
        return HttpResponseRedirect('/user/%s/' % object_id)

    user = Profile.objects.get(
        person=object_id,
        person__organization=request.user.get_profile().org_active
        ).user

    if not user.check_password(request.POST.get('actual_password_mini')):
        messages.error(request, _('Password Incorrect'))
        return HttpResponseRedirect('/user/%s/' % object_id)

    user.email = request.POST.get('email_mini')
    user.profile.temp = request.POST.get('email_mini')  # temporary field(LDAP)
    user.profile.save()
    user.save(force_update=True)

    messages.success(request, _('email updated successfully!'))
    # return render_to_response(
    #     '/user/%s/' % object_id,
    #     {'profile': user.profile},
    #     context_instance=RequestContext(request))
    # update_user(request, objecti_id)
    return HttpResponseRedirect('/user/%s/' % object_id)


@permission_required_with_403('users.users_write')
def set_form_user(request, object_id=0):
    array = {}  # json

    person = get_object_or_404(
        Person, pk=object_id,
        organization=request.user.get_profile().org_active
        )
    array[0] = slugify(person.name)
    array[1] = u'%s' % person.get_first_email()

    return HttpResponse(simplejson.dumps(array), mimetype='application/json')


@permission_required_with_403('users.users_write')
def order(request, profile_id=None):
    object = Profile.objects.get(
        pk=profile_id,
        person__organization=request.user.get_profile().org_active
        )
    if request.user.get_profile() == object:
        messages.success(request, ('Sorry, you can not disable yourself!'))
    else:
        if object.user.is_active:
            object.user.is_active = False
        else:
            object.user.is_active = True
            for i in object.user.registrationprofile_set.exclude(activation_key='ALREADY_ACTIVATED'):
                i.activation_key = 'ALREADY_ACTIVATED'
                i.save()

        object.user.save(force_update=True)
        messages.success(request, ('%s' % (_('User activated successfully') if object.user.is_active else _('User deactivated successfully'))))

    return HttpResponseRedirect('/user/%s/' % object.person.id)

@permission_required_with_403('organization.organization_read')
def username_is_available(request, user):
    """
    Check if username is available:
       0 = No
       1 = Yes
    """
    if User.objects.filter(username__iexact=user).count():
            return HttpResponse("0")
    else:
            return HttpResponse("1")
