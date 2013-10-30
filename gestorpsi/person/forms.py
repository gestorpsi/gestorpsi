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
from gestorpsi.client.models import Client
from gestorpsi.person.models import Person, Company, CompanyClient

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
        #fields = ('name', 'relation_level', 'responsible', 'active', 'comment')
    
    name = forms.CharField(label=_("Name"), 
                           required = True, 
                           widget=forms.TextInput(attrs={'class':'big tabtitle', 'maxlength': '50'}))
    nickname = forms.CharField(label=_("Nickname"), 
                               required = False, 
                               widget=forms.TextInput(attrs={'class':'big tabtitle', 'maxlength': '50'}))
    birthDate = forms.DateField(label=_("Birthday")+' ( dd/mm/yyyy )', 
                                required = False, 
                                widget=forms.DateInput(format =('%d/%m/%Y'), 
                                                       attrs={'class':'medium', 'maxlength': '10', 'mask': '99/99/9999'}),
                                )
    
    def clean_birthDate(self):
        try:
            return datetime.strptime(self.cleaned_data.get('birthDate'),'%d/%m/%Y')
        except:
            raise forms.ValidationError( _('Birthdate')+' inválida.' )
    
    def save(self, request, *args, **kwargs):
        if self.instance.pk is None:
            person = super(PersonForm, self).save(*args, **kwargs)
            return person
        else:
            """ AGE """
            dateBirthError = True
            dateBirth = request.POST.get('dateBirth', False)
            if request.POST.get('aprox', False) and request.POST.get('Years', False) and not dateBirth:
                    birthYear = (( int(datetime.now().strftime("%Y")) ) - ( int(request.POST.get('Years')) ) )
                    today = (datetime.now().strftime("%d/%m/"))
                    dt = "%s%s" % (today, birthYear)
                    person.birthDate = datetime.strptime(dt ,'%d/%m/%Y')
                    dateBirthError = False
            elif dateBirth:
                try:
                    person.birthDate = datetime.strptime(dateBirth, '%d/%m/%Y')
                    dateBirthError = False
                except:
                    pass
        
            if request.POST.get('aprox', False):
                person.birthDateSupposed = True
            else:
                person.birthDateSupposed = False
            """ AGE """
        
            person.gender = request.POST['gender']
            
            # maritalStatus
            try:
                if not (request.POST['maritalStatus']):
                    person.maritalStatus = None
                else:
                    person.maritalStatus = MaritalStatus.objects.get(pk = request.POST['maritalStatus'])
            except:
                person.maritalStatus = None
            
            try:
                person.birthPlace = City.objects.get(pk = request.POST['birthPlace'])
            except:
                person.birthPlace = None
                try:
                    person.birthForeignCity= request.POST['birthForeignCity']
                except:
                    person.birthForeignCity = None
                try:
                    person.birthForeignState= request.POST['birthForeignState']
                except:
                    person.birthForeignState = None
                try:
                    person.birthForeignCountry= request.POST['birthForeignCountry']
                except:
                    person.birthForeignCountry= None
        
            person.save()    
            user = request.user
            person.organization.add(user.get_profile().org_active)





