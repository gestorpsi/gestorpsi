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
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404
from django.conf import settings
from django.contrib.auth.models import User
from gestorpsi.organization.models import Organization
from gestorpsi.settings import DEBUG
from django.contrib.auth.forms import AuthenticationForm

# login_check decorator
# code from http://code.activestate.com/recipes/498217/
# changed by czd@gestorpsi.com.br

def login_check(f):
    @login_required
    def wrap(request, *args, **kwargs):
        if not DEBUG:
            if not request.is_ajax():
                raise Http404
        return f(request, *args, **kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap

def user_authentication(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        username = request.POST['username']
        password = request.POST['password']
        if(unblocked_user(username)):
            user = authenticate(username=username, password=password)   
            if user is not None:
                if user.is_active:
                    profile = user.get_profile()
                    request.session['temp_user'] = user                
                    clear_login(user)
                    if len(profile.organization.all()) > 1:                                                           
                        return render_to_response('registration/select_organization.html', { 'objects': user.organization.all()}) 
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

def user_organization(request):
    organization = Organization.objects.get(pk=request.POST['organization'])
    user = request.session['temp_user']
    del request.session['temp_user']        
    user.get_profile().org_active = organization    
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
    
def unblocked_user(user):
    filtered_user = User.objects.filter(username=user)
    if(len(filtered_user)):
        found_user = filtered_user[0]
        profile = found_user.get_profile()
        value = profile.try_login
        if (value >= settings.PASSWORD_RETIRES):            
            return False
        else:            
            return True
    else:
        return True

"""
+def get_object_or_new(klass, *args, **kwargs):
+    # bitbucket.org/offline/django-annoying/src/tip/annoying/functions.py
+    from django.shortcuts import _get_queryset
+    queryset = _get_queryset(klass)
+    try:
+        return queryset.get(*args, **kwargs)
+    except queryset.model.DoesNotExist:
+        return klass()
+
+def get_object_or_None(klass, *args, **kwargs):
+    from django.shortcuts import _get_queryset
+    queryset = _get_queryset(klass)
+    try:
+        return queryset.get(*args, **kwargs)
+    except queryset.model.DoesNotExist:
+        return None
+
+def unblocked_user(username):
+    user = get_object_or_None(User, username=username)
+    if user == None:
+        return False
+    else:
+        if user.get_profile().try_login >= settings.PASSWORD_RETIRES:
             return False
-        else:
+        else:
             return True
-    else:
-        return True
"""