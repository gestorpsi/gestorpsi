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
from django import forms
import reversion
from django.db import models
from django.utils.translation import ugettext as _
from gestorpsi.address.models import State, City
from smart_selects.db_fields import ChainedForeignKey
from django.core.validators import MaxValueValidator, MinLengthValidator


class BradescoBilletData(models.Model):
    cedente_nome = models.CharField(max_length=255, null=False, blank=False)
    cedente_nome.verbose_name = _("Seller's name")
    cedente_nome.help_text = _("Seller (company that will receive the money).")
    cedente_cnpj = models.CharField(max_length=20, null=False, blank=False)
    cedente_cnpj.widget = forms.TextInput(attrs={"mask": "99.999.999/9999-99",})
    cedente_cnpj.verbose_name = _("Seller's CNPJ")
    cedente_cnpj.help_text = ""
    
    sacadoravalista_nome = models.CharField(max_length=255, null=False, blank=False)
    sacadoravalista_nome.verbose_name = _("Guarantor's name")
    sacadoravalista_nome.help_text = _("Guarantor (the person that takes responsibility over the transaction).")
    sacadoravalista_cnpj = models.CharField(max_length=20, null=False, blank=False)
    sacadoravalista_cnpj.widget = forms.TextInput(attrs={"mask": "99.999.999/9999-99",})
    sacadoravalista_cnpj.verbose_name = _("Guarantor's CNPJ")
    sacadoravalista_cnpj.help_text = ""

    enderecosacaval_uf = models.ForeignKey(State, null=False, blank=False)
    enderecosacaval_uf.verbose_name = _("State")
    enderecosacaval_uf.help_text = _("State where the the guarantor lives.")
    enderecosacaval_localidade = ChainedForeignKey(City, chained_field='enderecosacaval_uf', chained_model_field='state', null=False, blank=False)
    enderecosacaval_localidade.verbose_name = _("City")
    enderecosacaval_localidade.help_text = _("City where the the guarantor lives.")
    enderecosacaval_cep = models.CharField(max_length=10, null=False, blank=False)
    enderecosacaval_cep.widget = forms.TextInput(attrs={"mask": "99999-999",})
    enderecosacaval_cep.verbose_name = _("CEP")
    enderecosacaval_cep.help_text = _("CEP - Postal code")
    enderecosacaval_bairro = models.CharField(max_length=255, null=False, blank=False)
    enderecosacaval_bairro.verbose_name = _("District")
    enderecosacaval_bairro.help_text = _("District where the guarantor lives")
    enderecosacaval_logradouro = models.CharField(max_length=255, null=False, blank=False)
    enderecosacaval_logradouro.verbose_name = _("Street")
    enderecosacaval_logradouro.help_text = _("Street where the guarantor lives.")
    enderecosacaval_numero = models.CharField(max_length=20, null=False, blank=False)
    enderecosacaval_numero.verbose_name = _("Number")
    enderecosacaval_numero.help_text = _("Number of the house where the guarantor lives.")

    contabancaria_numerodaconta = models.CharField(max_length=7, null=False, blank=False)
    contabancaria_numerodaconta.widget = forms.TextInput(attrs={"mask": "999999",})
    contabancaria_numerodaconta.verbose_name = _("Account")
    contabancaria_numerodaconta.help_text = _("Number of the bank account of the seller.")
    contabancaria_numerodaconta_digito = models.CharField(max_length=1, null=False, blank=False)
    contabancaria_numerodaconta_digito.widget = forms.TextInput(attrs={"mask": "9",})
    contabancaria_numerodaconta_digito.verbose_name = _("Verifier digit")
    contabancaria_numerodaconta_digito.help_text = _("Verifier digit of the bank account of the seller.")
    contabancaria_carteira = models.PositiveIntegerField(null=False, blank=False, validators=[MaxValueValidator(99)])
    contabancaria_carteira.verbose_name = _("Seller's wallet")
    contabancaria_carteira.help_text = _("Seller's bank wallet number")
    contabancaria_agencia = models.CharField(max_length=255, null=False, blank=False)
    contabancaria_agencia.widget = forms.TextInput(attrs={"mask": "9999",})
    contabancaria_agencia.verbose_name = _("Agency")
    contabancaria_agencia.help_text = _("Seller's account agency")
    contabancaria_agencia_digito = models.CharField(max_length=1, null=False, blank=False)
    contabancaria_agencia_digito.widget = forms.TextInput(attrs={"mask": "9",})
    contabancaria_agencia_digito.verbose_name = _("Agency digit")
    contabancaria_agencia_digito.help_text = _("Seller's account agency verifier digit")


    titulo_nossonumero = models.CharField(max_length=20, null=False, blank=False, validators=[MinLengthValidator(11)])
    titulo_nossonumero.verbose_name = _("\"Our number\"")
    titulo_nossonumero.help_text = _("Number registered in Bradesco to register the receiving of billets.")
    
    titulo_digitodonossonumero = models.CharField(max_length=1, null=False, blank=False)
    titulo_digitodonossonumero.widget = forms.TextInput(attrs={"mask": "9",})
    titulo_digitodonossonumero.verbose_name = _("\"Our number\" digit")
    titulo_digitodonossonumero.help_text = _("\"Our number\" digit")


    def __unicode__(self):
        return smart_str(self.cedente_nome)


reversion.register(BradescoBilletData)
