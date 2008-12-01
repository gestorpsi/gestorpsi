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

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.conf import settings
from gestorpsi.authentication.models import CustomUser
from gestorpsi.organization.models import Organization

def login_page(request):   
    return render_to_response('registration/login.html')

def user_authentication(request):
    username = request.POST['username']
    password = request.POST['password']
    if(unblocked_user(username)):
        user = authenticate(username=username, password=password)   
        if user is not None:
            if user.is_active:
                #login(request, user)
                request.session['temp_user'] = user                
                clear_login(user)               
                if len(user.organization.all()) > 1:                                                           
                    return render_to_response('registration/select_organization.html', { 'objects': user.organization.all()}) 
                    #print user , " - Organizacoes: " , user.organization
                    #return render_to_response('core/main.html', {'user': user })
                else:
                    number_org = []
                    number_org = user.organization.all()
                    user.org_active = number_org[0]
                    login(request, user)                                        
                    return HttpResponseRedirect('/')
                           
        else:
                set_trylogin(username)
                return render_to_response('registration/login.html', { 'message': "Invalid login" } )
    else:
        return render_to_response('registration/login.html', { 'message': "User blocked" } )
 
def logout_page(request):
    logout(request)    
    return HttpResponseRedirect('/') 

def user_organization(request):
    organization = Organization.objects.get(pk=request.POST['organization'])
    user = request.session['temp_user']
    del request.session['temp_user']        
    user.org_active = organization    
    login(request, user)           
    return HttpResponseRedirect('/') 


def set_trylogin(user):     
    filtered_user = CustomUser.objects.filter(username=user)
    if(len(filtered_user)):        
        found_user = filtered_user[0]    
        old_number = found_user.try_login
        old_number += 1
        found_user.try_login = old_number        
        found_user.save()
        print found_user," - tentativas: ", found_user.try_login   
       
def clear_login(user):
    user.try_login = 0
    user.save()
    print user," - tentativas: ", user.try_login
    
def change_password(user,current_password, new_password):    
    if check_password(current_password):   
        user.set_password(new_password)
        org = user.org_active
        user.org_active = None
        user.save()
        user.org_active = org       
    
def unblocked_user(user):
    filtered_user = CustomUser.objects.filter(username=user)
    if(len(filtered_user)):
        found_user = filtered_user[0]        
        value = found_user.try_login
        if (value >= settings.PASSWORD_RETIRES):            
            return False
        else:            
            return True
    else:
        return True

