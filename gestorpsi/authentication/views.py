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

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.conf import settings
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.forms.util import ErrorList
from django.utils.translation import ugettext as _
from django.contrib.auth.views import login as django_login
from gestorpsi.settings import SITE_DISABLED
from gestorpsi.organization.models import Organization
from gestorpsi.settings import DEBUG, ADMIN_URL
from gestorpsi.authentication.forms import RegistrationForm

# login_check decorator
# code from http://code.activestate.com/recipes/498217/
# changed by czd@gestorpsi.com.br

def login_check(f):
    @login_required
    def wrap(request, *args, **kwargs):
        return f(request, *args, **kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap


def user_authentication(request):
    if SITE_DISABLED:
        return render_to_response('core/site_disabled.html')
    if request.method != "POST":
        return render_to_response('registration/login.html', {'form': AuthenticationForm() })
    form = AuthenticationForm(data=request.POST)
    username = request.POST.get('username').strip().lower()
    password = request.POST.get('password')
    
    if (unblocked_user(username)):
        user = authenticate(username=username, password=password)
        
        # user does not exist
        if user is None:
            set_trylogin(username)
            form_messages = _('Invalid username or password')
            return render_to_response('registration/login.html', {'form': form, 'form_messages': form_messages })
        else:
            request.session['user_aux_id'] = user.id
        if user.is_staff or user.is_superuser:
            login(request, user)
            return HttpResponseRedirect(ADMIN_URL)

        # user has not confirmed registration yet
        if user.registrationprofile_set.all()[0].activation_key != 'ALREADY_ACTIVATED':
            form_messages = _('Your account has not been confirmated yet. Please check your email and use your activation code to continue')
            return render_to_response('registration/login.html', {'form':form, 'form_messages': form_messages })
        
        if not user.is_active:
            form_messages = _('Your account has been disable. Please contact our support')
            return render_to_response('registration/login.html', {'form':form, 'form_messages': form_messages })
        else:
            clear_login(user)
            profile = user.get_profile()
            if profile.organization.distinct().count() > 1:
                try:
                    organization = profile.organization.get(short_name__iexact = request.POST.get('shortname'))
                    profile.org_active = organization
                    profile.save()
                    user.groups.clear()
                    for role in user.get_profile().role_set.filter(organization=organization):
                        user.groups.add(role.group)
                    login(request, user)
                    return HttpResponseRedirect('/')
                except Organization.DoesNotExist:
                    request.session['temp_user'] = user
                    return render_to_response('registration/select_organization.html', { 'objects': profile.organization.distinct() })
            login(request, user)
            return HttpResponseRedirect(request.POST.get('next') or '/')

def user_organization(request):
    organization = Organization.objects.get(pk=request.POST.get('organization'))
    user = request.session['temp_user']
    del request.session['temp_user']        
    user.get_profile().org_active = organization
    user.get_profile().save()

    """ Update roles according to selected organization """
    user.groups.clear()
    for role in user.get_profile().role_set.filter(organization=organization):
        user.groups.add(role.group)

    login(request, user)           
    return HttpResponseRedirect('/')

def old_user_authentication(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        username = request.POST.get('username').strip().lower()
        password = request.POST.get('password')
        if(unblocked_user(username)):
            user = authenticate(username=username, password=password)   
            if user is not None:
                if user.is_active:
                    profile = user.get_profile()
                    request.session['temp_user'] = user                
                    clear_login(user)
                    if len(profile.organization.all()) > 1:                                                           
                        return render_to_response('registration/select_organization.html', { 'objects': profile.organization.all()}) 
                    else:
                        number_org = []
                        number_org = profile.organization.all()
                        profile.org_active = number_org[0]
                        login(request, user)                                        
                        return HttpResponseRedirect('/')
            else:
                    set_trylogin(username)
                    return render_to_response('registration/login.html', {'form':form })
    else:
        form = AuthenticationForm()
        return render_to_response('registration/login.html', { 'form':form } )

def old_user_organization(request):
    organization = Organization.objects.get(pk=request.POST.get('organization'))
    user = request.session['temp_user']
    del request.session['temp_user']        
    user.get_profile().org_active = organization
    user.get_profile().save()
    login(request, user)           
    return HttpResponseRedirect('/') 


def set_trylogin(user):     
    filtered_user = User.objects.filter(username=user)
    if(len(filtered_user)):        
        found_user = filtered_user[0]    
        old_number = found_user.get_profile().try_login
        old_number += 1
        found_user.get_profile().try_login = old_number
        found_user.save()

def clear_login(user):
    user.get_profile().try_login = 0
    user.save()
    
def change_password(user,current_password, new_password):    
    if check_password(current_password):   
        user.set_password(new_password)
        org = user.get_profile().org_active
        user.get_profile().org_active = None
        user.save()
        user.get_profile().org_active = org       
    
def unblocked_user(username):
    user = get_object_or_404(User, username=username)
    
    if user.is_staff or user.is_superuser:
        return True
    
    profile = user.get_profile()
    value = profile.try_login
    if (value >= settings.PASSWORD_RETIRES):            
        return False
    
    return True

'''
from django-registration
'''
def register(request, success_url=None,
             form_class=RegistrationForm,
             template_name='registration/registration_form.html',
             extra_context=None):
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if Organization.objects.filter(short_name__iexact = slugify(request.POST.get('shortname'))):
            form = form_class(data=request.POST) # organization already exists, escaping .. 
            error_msg = _(u"Informed organization is already registered. Please choice another name here or login with an existing account")
            form.errors["organization"] = ErrorList([error_msg])
        elif request.POST.get('username') != slugify(request.POST.get('username')):
            error_msg = _(u"Enter a valid username.")
            form.errors["username"] = ErrorList([error_msg])
        else:
            if form.is_valid():
                new_user = form.save()
                return HttpResponseRedirect(success_url or reverse('gcm-registration-complete'))
    else:
        form = form_class()
    
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return render_to_response(template_name,
                              { 'form': form },
                              context_instance=context)

def gestorpsi_login(request, *args, **kwargs):
    if SITE_DISABLED:
        return render_to_response('core/site_disabled.html')
    return django_login(request, *args, **kwargs)
