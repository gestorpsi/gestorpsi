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

from registration.forms import RegistrationForm as RegistrationRegistrationForm
from registration.models import RegistrationProfile

from gestorpsi.organization.models import Organization
from gestorpsi.place.models import Place, PlaceType, Room, RoomType
from gestorpsi.authentication.models import Profile, Role
from gestorpsi.person.models import Person
from gestorpsi.careprofessional.models import CareProfessional, ProfessionalProfile, ProfessionalIdentification

from gestorpsi.gcm.models import Plan
from gestorpsi.gcm.forms import fields

from gestorpsi.phone.models import Phone
from gestorpsi.address.models import State, City, Address, AddressType

from gestorpsi.document.models import TypeDocument, Document

attrs_dict = { 'class': 'required' }

class AuthenticationRegistrationForm(RegistrationRegistrationForm):
    name = forms.CharField(label=_('Name'), help_text=_('Responsible professional name'))
    email = forms.EmailField(label=_('Email'), help_text=_('Your email address'))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False), label=_('Password'), help_text=_('Choice one password'))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False), label=_('Password (again)'), help_text=_('Type password again'))
    username = forms.CharField(label=_('Username'), help_text=_('Choice one unique identifier'))
    organization = forms.CharField(label=_('Organization'), help_text=_('Name of your organization'))
    shortname = forms.CharField(label=_('Short Name'), help_text=_('Shortname of your organization'))

    def save(self, send_email=True):
        user = RegistrationProfile.objects.create_inactive_user(username=self.cleaned_data['username'],
                                                                    password=self.cleaned_data['password1'],
                                                                    email=self.cleaned_data['email'],
                                                                    site=None,
                                                                    send_email=send_email
                                                                    )
        user.username = user.username.strip().lower()
        user.save()         # remove spaces from username and change all to lowercase
        profile = Profile(user=user)
        profile.save()
        organization = Organization.objects.create( #create organization
            name = self.cleaned_data['organization'],
            trade_name = self.cleaned_data['organization'],
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

        person = Person.objects.create(name=self.cleaned_data['name'], user=user) #, organization=organization)
        person.organization.add(organization)
        profile.org_active = organization                  #set org as active
        profile.temp = self.cleaned_data['password1']      # temporary field (LDAP)
        profile.person = person
        profile.save()
        
        try:
            admin_role = Group.objects.get(name='administrator')
            Role.objects.create(profile=profile, organization=organization, group=admin_role)
            profile.user.groups.add(admin_role)
        except:
            pass
        try:
            professional_role = Group.objects.get(name='professional')
            Role.objects.create(profile=profile, organization=organization, group=professional_role)
            profile.user.groups.add(professional_role)
        except:
            pass

        careprof = CareProfessional()
        careprof.person = person
        pp = ProfessionalProfile()
        pi = ProfessionalIdentification()
        pp.save()
        pi.save()
        careprof.professionalProfile = pp
        careprof.professionalIdentification = pi
        careprof.save()

        return organization


"""
    Tiago de Souza Moraes
    Change 11 08 2014
"""
class RegistrationForm(AuthenticationRegistrationForm):

    plan = forms.ModelChoiceField(label=_('Access Plan'), help_text=_('Choice one access plan'), queryset=Plan.objects.filter(active=True))
    phone = forms.CharField(max_length=15, label=_('Phone Number'), help_text=_('Enter your phone number with area code here'), widget=forms.TextInput(attrs={'mask':'(99) 9999-9999?9',}))
    cpf = fields.CPFField(label=_('CPF Number'), help_text=_('Enter your CPF number here'), widget=forms.TextInput(attrs={'mask':'999.999.999-99',}))
    address = forms.CharField(max_length=255, label=_('Address Street'), help_text=_('Enter your address here'))
    address_number = forms.CharField(max_length=30, label=_('Address Number'), help_text=_('Enter your address number here'))
    zipcode = forms.CharField(max_length=30, label=_('ZIP Code'), help_text=_('Enter your ZIP Code here'), widget=forms.TextInput( attrs={'mask':'99999-999'} ) )
    state = forms.ModelChoiceField(label=_('State/Region'), help_text=_('Enter your state/region here'), queryset=State.objects.all(), widget=forms.Select(attrs={'style':'width:265px;', 'class':'city_search'}))
    city = forms.ModelChoiceField( label=_('City'), help_text=_('Enter your state/region here'), queryset=City.objects.all(), widget=forms.Select(attrs={'style':'width:265px;'}) )

    def save(self, request, *args, **kwargs):
        organization = super(RegistrationForm, self).save(False, *args, **kwargs) # send_email = False 

        # add phone number to 'first' professional registered
        if self.cleaned_data['phone']:
            p = Phone()
            p.area = self.cleaned_data['phone'][1:3]
            p.phoneNumber = self.cleaned_data['phone'][5:15]
            p.phoneType_id = 2
            person = organization.care_professionals()[0]
            person.phones.add(p)
            
        # add cpf number to 'first' professional registered
        if self.cleaned_data['cpf']:
            d = Document()
            t = TypeDocument.objects.get(description='CPF')
            d.typeDocument_id = t.id
            d.document = self.cleaned_data['cpf']
            person.document.add(d)

        # add address to 'first' professional registered
        if self.cleaned_data['address']:
            a = Address()
            at = AddressType.objects.get(description='Comercial')
            a.addressType_id = at.id
            a.addressLine1 = self.cleaned_data['address']
            a.addressNumber = self.cleaned_data['address_number']
            a.zipCode = self.cleaned_data['zipcode']
            a.city_id = request.POST.get('city')
            person.address.add(a)
