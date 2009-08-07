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
from django.template.defaultfilters import slugify
from django.contrib.auth.models import Group
from registration.forms import RegistrationForm
from registration.models import RegistrationProfile
from gestorpsi.organization.models import Organization
from gestorpsi.place.models import Place, PlaceType, Room, RoomType
from gestorpsi.authentication.models import Profile, Role
from gestorpsi.person.models import Person
from gestorpsi.careprofessional.models import CareProfessional, ProfessionalProfile, ProfessionalIdentification

attrs_dict = { 'class': 'required' }

class RegistrationForm(RegistrationForm):
    name = forms.CharField(label=_('Name'), help_text=_('Responsible professional name'))
    email = forms.EmailField(label=_('Email'), help_text=_('Your email address'))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False), label=_('Password'), help_text=_('Choice one password'))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False), label=_('Password (again)'), help_text=_('Type password again'))
    username = forms.CharField(label=_('Username'), help_text=_('Choice one unique identifier'))
    organization = forms.CharField(label=_('Organization'), help_text=_('Name of your organization'))
    shortname = forms.CharField(label=_('Short Name'), help_text=_('Shortname of your organization'))

    def save(self):
        user = super(RegistrationForm, self).save() #create user
        user.username = user.username.strip().lower()
        user.save()         # remove spaces from username and change all to lowercase
        profile = Profile(user=user)
        profile.save()
        organization = Organization.objects.create( #create organization
            name = self.cleaned_data['organization'],
            short_name = slugify(self.cleaned_data['shortname']),
        )
        default_place = Place.objects.create(         #create default place
            label = organization.name,                # use same name as label
            active = True,
            place_type = PlaceType.objects.get(description='Matriz'), # mandatory field
            organization = organization,              # link place to this organization
        )
        default_room = Room.objects.create(
            description = 'Sala 1',
            place = default_place,
            room_type=RoomType.objects.all()[0],
        )

        person = Person.objects.create(name=self.cleaned_data['name']) #, organization=organization)
        person.organization.add(organization)
        profile.org_active = organization                  #set org as active
        profile.temp = self.cleaned_data['password1']      # temporary field (LDAP)
        profile.person = person
        profile.save()
                
        admin_role = Group.objects.get(name='administrator')
        Role.objects.create(profile=profile, organization=organization, group=admin_role)
        profile.user.groups.add(admin_role)

        careprof = CareProfessional()
        careprof.person = person
        careprof.professionalProfile = ProfessionalProfile.objects.create()
        careprof.professionalIdentification = ProfessionalIdentification.objects.create(registerNumber='')
        careprof.save()

