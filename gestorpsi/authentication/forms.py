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


from django import forms
from django.utils.translation import ugettext_lazy as _
from registration.forms import RegistrationForm
from registration.models import RegistrationProfile
from gestorpsi.organization.models import Organization
from gestorpsi.authentication.models import Profile

attrs_dict = { 'class': 'required' }

class RegistrationForm(RegistrationForm):
    email = forms.EmailField(label=_('Email'), help_text=_('Your email address'))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False), label=_('Password'), help_text=_('Choice one password'))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False), label=_('Password (again)'), help_text=_('Type password again'))
    username = forms.CharField(label=_('Username'), help_text=_('Choice one unique identifier'))
    organization = forms.CharField(label=_('Organization'), help_text=_('Name of your organization'))

    def save(self, profile_callback=None):
        user = super(RegistrationForm, self).save(profile_callback=profile_callback) #create user
        profile = user.get_profile()
        organization = Organization.objects.create( #create organization
            name = self.cleaned_data['organization'],
        )
        profile.organization.add(organization) #link organization to profile
        profile.org_active = organization #set org as active
        profile.save() #save it
        
