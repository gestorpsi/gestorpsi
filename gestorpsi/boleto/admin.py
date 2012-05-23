# -*- coding: utf-8 -*-

"""
Copyright (C) 2012 GestorPsi

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

"""
   This file contains all configurations for Admin Interface
   I{These models were created only for testing purposes}
   @author: Sergio Durand
   @version: 1.0
"""

from gestorpsi import settings
from django.contrib import admin
from gestorpsi.boleto.models import BradescoBilletData
from django import forms
from django.db import models
from gestorpsi.address.models import State, City
from django.utils.translation import ugettext as _
from smart_selects.db_fields import ChainedForeignKey
from django.core.validators import BaseValidator, MinLengthValidator, MaxValueValidator
from django.core import exceptions
from django.utils.encoding import smart_str

def CNPJValidator(value):
    def generate_digits(value):
        cnpj = value
        if len( cnpj ) != 18:
            return False;
        else:
            soma = 0
            soma += int(cnpj[0])*5
            soma += int(cnpj[1])*4
            soma += int(cnpj[3])*3
            soma += int(cnpj[4])*2
            soma += int(cnpj[5])*9
            soma += int(cnpj[7])*8
            soma += int(cnpj[8])*7
            soma += int(cnpj[9])*6
            soma += int(cnpj[11])*5
            soma += int(cnpj[12])*4
            soma += int(cnpj[13])*3
            soma += int(cnpj[14])*2
            
            resto = soma % 11
            if resto < 2:
                digito1 = 0
            else:
                digito1 = 11 - resto
            
            soma = 0
            soma += int(cnpj[0])*6
            soma += int(cnpj[1])*5
            soma += int(cnpj[3])*4
            soma += int(cnpj[4])*3
            soma += int(cnpj[5])*2
            soma += int(cnpj[7])*9
            soma += int(cnpj[8])*8
            soma += int(cnpj[9])*7
            soma += int(cnpj[11])*6
            soma += int(cnpj[12])*5
            soma += int(cnpj[13])*4
            soma += int(cnpj[14])*3
            soma += int(cnpj[16])*2 
            
            resto = soma % 11
            if resto < 2:
                digito2 = 0
            else:
                digito2 = 11 - resto
            return str(digito1) + str(digito2)

    def validate(digits, value):
        return digits == ( value[16] + value[17] ) 

    digits = generate_digits(value)
    if not validate(digits, value):
        raise exceptions.ValidationError( _(u'The CNPJ %s is not valid (right digits for testing purpose: %s).' % (value, digits)) )  
    


class BradescoBilletDataAdminForm(forms.ModelForm):

    cedente_cnpj = forms.CharField(widget = forms.TextInput(attrs={"mask": "99.999.999/9999-99",}), validators=[CNPJValidator]  )
    sacadoravalista_cnpj = forms.CharField(widget = forms.TextInput(attrs={"mask": "99.999.999/9999-99",}), validators=[CNPJValidator] )
    enderecosacaval_cep = forms.CharField(widget = forms.TextInput(attrs={"mask": "99999-999",}) )
    contabancaria_numerodaconta = forms.CharField(widget = forms.TextInput(attrs={"mask": "999999",}) )
    contabancaria_numerodaconta_digito = forms.CharField(widget = forms.TextInput(attrs={"mask": "9",}) )
    contabancaria_agencia = forms.CharField(widget = forms.TextInput(attrs={"mask": "9999",}) )
    contabancaria_agencia_digito = forms.CharField(widget = forms.TextInput(attrs={"mask": "9",}) )
    titulo_digitodonossonumero = forms.CharField(widget = forms.TextInput(attrs={"mask": "9",}) )
    
    
    titulo_nossonumero = models.CharField(max_length=20, null=False, blank=False, validators=[MinLengthValidator(11)])
    cedente_nome = models.CharField(max_length=255, null=False, blank=False)
    sacadoravalista_nome = models.CharField(max_length=255, null=False, blank=False)
    enderecosacaval_bairro = models.CharField(max_length=255, null=False, blank=False)
    enderecosacaval_logradouro = models.CharField(max_length=255, null=False, blank=False)
    enderecosacaval_numero = models.CharField(max_length=20, null=False, blank=False)
    enderecosacaval_uf = models.ForeignKey(State, null=False, blank=False)
    enderecosacaval_localidade = ChainedForeignKey(City, chained_field='enderecosacaval_uf', chained_model_field='state', null=False, blank=False)
    contabancaria_carteira = models.PositiveIntegerField(null=False, blank=False, validators=[MaxValueValidator(99)])
    cedente_nome.label = _("Seller's name")
    cedente_nome.help_text = _("Seller (company that will receive the money).")
    cedente_cnpj.label = _("Seller's CNPJ")
    cedente_cnpj.help_text = ""
    sacadoravalista_nome.label = _("Guarantor's name")
    sacadoravalista_nome.help_text = _("Guarantor (the person that takes responsibility over the transaction).")
    sacadoravalista_cnpj.label = _("Guarantor's CNPJ")
    sacadoravalista_cnpj.help_text = ""
    enderecosacaval_uf.label = _("State")
    enderecosacaval_uf.help_text = _("State where the the guarantor lives.")
    enderecosacaval_localidade.label = _("City")
    enderecosacaval_localidade.help_text = _("City where the the guarantor lives.")
    enderecosacaval_cep.label = _("CEP")
    enderecosacaval_cep.help_text = _("CEP - Postal code")
    enderecosacaval_bairro.label = _("District")
    enderecosacaval_bairro.help_text = _("District where the guarantor lives")
    enderecosacaval_logradouro.label = _("Street")
    enderecosacaval_logradouro.help_text = _("Street where the guarantor lives.")
    enderecosacaval_numero.label = _("Number")
    enderecosacaval_numero.help_text = _("Number of the house where the guarantor lives.")
    contabancaria_numerodaconta.label = _("Account")
    contabancaria_numerodaconta.help_text = _("Number of the bank account of the seller.")
    contabancaria_numerodaconta_digito.label = _("Verifier digit")
    contabancaria_numerodaconta_digito.help_text = _("Verifier digit of the bank account of the seller.")
    contabancaria_carteira.label = _("Seller's wallet")
    contabancaria_carteira.help_text = _("Seller's bank wallet number")
    contabancaria_agencia.label = _("Agency")
    contabancaria_agencia.help_text = _("Seller's account agency")
    contabancaria_agencia_digito.label = _("Agency digit")
    contabancaria_agencia_digito.help_text = _("Seller's account agency verifier digit")
    titulo_nossonumero.label = _("\"Our number\"")
    titulo_nossonumero.help_text = _("Number registered in Bradesco to register the receiving of billets.")
    titulo_digitodonossonumero.label = _("\"Our number\" digit")
    titulo_digitodonossonumero.help_text = _("\"Our number\" digit")


    class Meta:
        model = BradescoBilletData

    class Media:
        js = (
              settings.MEDIA_URL+"js/jquery.maskedinput-1.1.3.pack.js",
              settings.MEDIA_URL+"js/boleto.admin.js",
        )
        css = {
              "all": (settings.MEDIA_URL+"css/boleto.admin.css", )
        }




class BradescoBilletDataAdmin(admin.ModelAdmin):
    model = BradescoBilletData

        
    form = BradescoBilletDataAdminForm

    #formfield_overrides = {
    #    models.TextField: {'widget': RichTextEditorWidget},
    #}



admin.site.register(BradescoBilletData, BradescoBilletDataAdmin)
