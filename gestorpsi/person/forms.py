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
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

from gestorpsi.client.models import Client
from gestorpsi.person.models import Person, Company, CompanyClient, MaritalStatus
from gestorpsi.address.models import Country, State, AddressType, City

MARITAL_STATUS_CHOICES = ( (p.id, p.description) for p in MaritalStatus.objects.all() )
COUNTRY_CHOICES = ( ((p.id, p.name) for p in Country.objects.all()) )
STATE_SHORT_CHOICES = ( (p.id, p.shortName) for p in State.objects.all() )
CITY_CHOICES = ( (p.id, p.name) for p in City.objects.all() )

class CompanyForm(forms.ModelForm):
    cnae_class = forms.CharField(label=_('CNAE Class Code'), required=False, widget=forms.TextInput(attrs={'mask':'9999-9/99'}))
    class Meta:
        model = Company
        fields = ('size', 'cnae_class', )

class CompanyClientForm(forms.ModelForm):
    name = forms.CharField(required = True, widget=forms.TextInput(attrs={'class':'extrabig'}))

    class Meta:
        model = CompanyClient
        fields = ('name', 'responsible', 'active')

    def save(self, request, client, *args, **kwargs):
        company_client = super(CompanyClientForm, self).save(commit=False, *args, **kwargs)
        company_client.company = client.person.company

        if not request.POST.get('client_id'): # client and person is new, lets create it before
            person = Person(name=request.POST.get('name'))
            person.save()
            person.organization.add(request.user.get_profile().org_active.id)
            client_related = Client(person=person, idRecord = request.user.get_profile().org_active.last_id_record + 1)
            client_related.save()
            company_client.active = True
        else: # client already exist, let's create or edit some existing relation
            if not request.POST.get('client_id') in [i.client.id for i in client.person.company.companyclient_set.all()] and not request.POST.get('active'): # relation already exists, let's edit it
                company_client.active = True
            client_related = Client.objects.get(pk=request.POST.get('client_id'), person__organization = request.user.get_profile().org_active)

        company_client.client = client_related
        company_client.responsible = False if not request.POST.get('responsible') else True
        company_client.save()

        return company_client


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('birthDateSupposed', 'years', 'name', 'nickname', 'birthDate', 'birthPlace', 
                  'gender', 'maritalStatus',  'comments', 'active', 'organization', 'birthForeignCity', 
                  'birthForeignState', 'birthCountry', 'birthState')
    
    def __init__(self, *args, **kwargs):
            if 'initial' not in kwargs:
                kwargs['initial'] = {}
            if 'instance' in kwargs:
                instance = kwargs['instance']
                if instance.birthDateSupposed:
                    if instance.birthDate:
                        d = datetime.today()
                        kwargs['initial']['years'] = (d.year - instance.birthDate.year) - int((d.month, d.day) < (instance.birthDate.month, instance.birthDate.day))
                if instance.birthPlace:
                    kwargs['initial']['birthPlaceState'] = instance.birthPlace.state
            super(PersonForm, self).__init__(*args, **kwargs)
            
            if self.errors:
                for f_name in self.fields:
                    if f_name in self.errors:
                        classes = self.fields[f_name].widget.attrs.get('class', '')
                        classes += ' formError'
                        self.fields[f_name].widget.attrs['class'] = classes
    
    
    
    name = forms.CharField(label=_("Name"), 
                           required = True, 
                           widget=forms.TextInput(attrs={'class':'big tabtitle', 'maxlength': '50'}))
    
    nickname = forms.CharField(label=_("Nickname"), 
                               required = False, 
                               widget=forms.TextInput(attrs={'class':'big tabtitle', 'maxlength': '50'}))
    
    birthDate = forms.DateField(label=_("Birthday")+' ( dd/mm/yyyy )', 
                                required = False, 
                                widget=forms.DateInput(#format =('%d/%m/%Y'), 
                                                       attrs={'class':'medium', 'maxlength': '10', 'mask': '99/99/9999'}),
                                )
    
    maritalStatus = forms.IntegerField(label=_('Marital Status'),
                                       required=False,
                                       widget=forms.Select(choices=MARITAL_STATUS_CHOICES,
                                                           attrs={'class':'select extramedium',}))
    
    years = forms.IntegerField(label=_('Age'),
                               required=False,
                               widget=forms.TextInput(attrs={'class':'small',}))
    
    birthDateSupposed = forms.BooleanField(label=_('Birthdate supposed'),
                                           required=False,
                                           widget=forms.CheckboxInput(attrs={}))
    
    birthPlace = forms.IntegerField(label=_('City'),
                                    required=False,
                                    widget=forms.Select(choices=CITY_CHOICES,
                                                   attrs={'class':'extramedium',}))
    birthCountry = forms.IntegerField(label=_('Country'),
                                      required=False,
                                      widget=forms.Select(choices=COUNTRY_CHOICES,
                                                   attrs={'class':'select country',}))
    birthState = forms.IntegerField(label=_('State'),
                                     required=False,
                                     widget=forms.Select(choices=STATE_SHORT_CHOICES,
                                                   attrs={'class':'city_search extrasmall',}))
    birthForeignCity = forms.CharField(label=_('City'),
                                             required=False,
                                             widget=forms.TextInput(attrs={'class':'extramedium', 'maxlength': '100'}))
    birthForeignState = forms.CharField(label=_('State'),
                                             required=False,
                                             widget=forms.TextInput(attrs={'class':'extrasmall', 'maxlength': '100'}))
    birthForeignCountry = forms.CharField(max_length=100,
                                          label=_('Country'),
                                          required=False,
                                          widget=forms.TextInput(attrs={'class':'select country',}))
        
    
    def clean(self):
        self.cleaned_data = super(PersonForm, self).clean()
        #raise Exception( self.cleaned_data )
        #if self.cleaned_data.get('birthDate'):# and 'birthDate' in self._errors:
        #    del self._errors['director']
        #    raise Exception( self.cleaned_data.get('birthDate') )
        return self.cleaned_data 
    
        if not 'instance' in kwargs:
            if kwargs['instance'].birthDateSupposed:
                self.fields['birthDate'].widget.attrs['disabled'] = 'disabled'
            else:
                self.fields['years'].widget.attrs['disabled'] = 'disabled'
    
    def clean_birthDate(self):
        if self.cleaned_data.get('birthDateSupposed', False):
            try:
                dt = date.today() - relativedelta( years=int(self.cleaned_data.get('years')) )
                return str(dt)
            except:
                raise forms.ValidationError( _('Invalid age provided') )
        else:
            bday = datetime.strptime( str(self.cleaned_data.get('birthDate')), '%Y-%d-%m')
            bday = '-'.join([str(bday.year), str(bday.month), str(bday.day)])
            return bday
    
    def clean_birthState(self):
        try:
            return State.objects.get( id=self.cleaned_data.get('birthState') )
        except:
            raise forms.ValidationError( _('Invalid state provided') )
    
    def clean_birthCountry(self):
        try:
            return Country.objects.get( id=self.cleaned_data.get('birthCountry') )
        except:
            raise forms.ValidationError( _('Invalid country provided') )
    
    def clean_years(self):
        if self.cleaned_data.get('birthDateSupposed', False):
            try:
                idade = int( self.cleaned_data.get('years') )
            except:
                raise forms.ValidationError( _('Invalid age provided') )
            if idade > 0:
                return idade
            else:
                raise forms.ValidationError( _('Invalid age provided') )
        else:
            try:
                d = datetime.now()
                temp = self.cleaned_data.get('birthDate')
                if temp is not None:
                    bday = datetime.strptime(temp, '%Y-%d-%m')
                    return (d.year - bday.year) - int((d.month, d.day) < (bday.month, bday.day))
                else:
                    return None
            except:
                raise forms.ValidationError( _('Invalid Birthdate') )

    
    def clean_maritalStatus(self):
        try:
            return MaritalStatus.objects.get(pk=self.cleaned_data.get('maritalStatus'))
        except:
            return None
    
    def clean_birthPlace(self):
        try:
            return City.objects.get( pk=self.cleaned_data.get('birthPlace') )
        except:
            raise forms.ValidationError( _('City not selected') )
    def clean_birthForeignCountry(self):
        try:
            return int( self.cleaned_data.get('birthForeignCountry') )
        except:
            return None
        
        
    def render(self):
        form = self
        return render_to_string('person/forms/personform.html', locals())
    def __str__(self):
        return self.render()
    def __unicode__(self):
        return self.render()
    
    def save(self, request, *args, **kwargs):
        person = super(PersonForm, self).save(*args, **kwargs)
        if self.instance.pk is None:
            # Id Record
            org = get_object_or_404('organization.Organization', pk=request.user.get_profile().org_active.id )
            object.idRecord = org.last_id_record + 1
            org.last_id_record = org.last_id_record + 1
            org.save()
        else:
            person.organization.add(request.user.get_profile().org_active)
        
        if person.birthDateSupposed == True:
            dt = datetime.now() - relativedelta(years=person.years) 
            person.birthDate = dt
            self.instance.birthDate = temp
        else:
            d = datetime.now()
            temp = person.birthDate
            if temp is not None:
                temp = (d.year - temp.year) - int((d.month, d.day) < (temp.month, temp.day))
            else:
                temp = None
            self.instance.years = temp
            person.years = temp
        person.save()
        return person




