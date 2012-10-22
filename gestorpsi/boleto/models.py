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
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.utils.encoding import smart_str
from datetime import datetime

from gestorpsi.boleto.helpers import RetornoBradescoProcessor

from gestorpsi.settings import PROJECT_ROOT_PATH
import os


INSCRIPTION_DEFAULT_VALUE = 35.00
BANK_CHOICES = (
    ('bradesco', 'Bradesco'),
    #('bb', 'Banco do Brasil'),
)


class BradescoBilletData(models.Model):
    inscription_default_value = models.DecimalField(max_digits=19, decimal_places=10, default=INSCRIPTION_DEFAULT_VALUE)
    inscription_default_value.verbose_name = _("Default inscription tax")
    inscription_default_value.help_text = _("Value charged on the user to make their inscription on the system.")
    
    default_payment_day = models.PositiveIntegerField(validators=[MaxValueValidator(28), MinValueValidator(1)], default=10)
    default_payment_day.verbose_name = _("Default payment day")
    default_payment_day.help_text= _("The default day in which the billets have to be paid by all the organizations (if they define another one that one will be preferred).")
    
    default_second_copy_days = models.PositiveIntegerField(validators=[MaxValueValidator(28), MinValueValidator(1)], default=7)
    default_second_copy_days.verbose_name = _("Second copy tolerance time")
    default_second_copy_days.help_text= _("The default amount of days that will be added to a second copy of a billet.")
    
    cedente_nome = models.CharField(max_length=255, null=True, blank=True)
    cedente_nome.verbose_name = _("Seller's name")
    cedente_nome.help_text = _("Seller (company that will receive the money).")
    cedente_cnpj = models.CharField(max_length=20, null=True, blank=True)
    cedente_cnpj.widget = forms.TextInput(attrs={"mask": "99.999.999/9999-99",})
    cedente_cnpj.verbose_name = _("Seller's CNPJ")
    cedente_cnpj.help_text = ""
    
    sacadoravalista_nome = models.CharField(max_length=255, null=True, blank=True)
    sacadoravalista_nome.verbose_name = _("Guarantor's name")
    sacadoravalista_nome.help_text = _("Guarantor (the person that takes responsibility over the transaction).")
    sacadoravalista_cnpj = models.CharField(max_length=20, null=True, blank=True)
    sacadoravalista_cnpj.widget = forms.TextInput(attrs={"mask": "99.999.999/9999-99",})
    sacadoravalista_cnpj.verbose_name = _("Guarantor's CNPJ")
    sacadoravalista_cnpj.help_text = ""

    enderecosacaval_uf = models.ForeignKey(State, null=True, blank=True)
    enderecosacaval_uf.verbose_name = _("State")
    enderecosacaval_uf.help_text = _("State where the the guarantor lives.")
    enderecosacaval_localidade = ChainedForeignKey(City, chained_field='enderecosacaval_uf', chained_model_field='state', null=True, blank=True)
    enderecosacaval_localidade.verbose_name = _("City")
    enderecosacaval_localidade.help_text = _("City where the the guarantor lives.")
    enderecosacaval_cep = models.CharField(max_length=10, null=True, blank=True)
    enderecosacaval_cep.widget = forms.TextInput(attrs={"mask": "99999-999",})
    enderecosacaval_cep.verbose_name = _("CEP")
    enderecosacaval_cep.help_text = _("CEP - Postal code")
    enderecosacaval_bairro = models.CharField(max_length=255, null=True, blank=True)
    enderecosacaval_bairro.verbose_name = _("District")
    enderecosacaval_bairro.help_text = _("District where the guarantor lives")
    enderecosacaval_logradouro = models.CharField(max_length=255, null=True, blank=True)
    enderecosacaval_logradouro.verbose_name = _("Street")
    enderecosacaval_logradouro.help_text = _("Street where the guarantor lives.")
    enderecosacaval_numero = models.CharField(max_length=20, null=True, blank=True)
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


    titulo_nossonumero = models.CharField(max_length=11, null=False, blank=False, validators=[MinLengthValidator(11)])
    titulo_nossonumero.verbose_name = _("\"Our number\"")
    titulo_nossonumero.help_text = _("Number registered in Bradesco to register the receiving of billets.")
    
    titulo_digitodonossonumero = models.CharField(max_length=1, null=False, blank=False)
    titulo_digitodonossonumero.widget = forms.TextInput(attrs={"mask": "9",})
    titulo_digitodonossonumero.verbose_name = _("\"Our number\" digit")
    titulo_digitodonossonumero.help_text = _("\"Our number\" digit")


    def __unicode__(self):
        return smart_str(self.cedente_nome)
    def save(self, *args, **kwargs):
        if self.inscription_default_value is None or len(self.inscription_default_value) == 0:
            self.inscription_default_value = str(INSCRIPTION_DEFAULT_VALUE)
        super(Organization, self).save(*args, **kwargs)

reversion.register(BradescoBilletData)


class ReturnFile(models.Model):
    date_import = models.DateTimeField(default=datetime.today, verbose_name=_("Data arquivo"), blank=True, null=True)
    arquivo_retorno = models.FileField(upload_to='arquivos_retorno', verbose_name=_("Arquivo"))
    banco = models.CharField(_('Banco'), max_length=20, null=True, blank=True,choices=BANK_CHOICES, default='bradesco')
    #numero registros
    #numero linhas
    
    def save(self, force_insert=False, force_update=False):
        super(ReturnFile, self).save()

        if self.banco == 'bradesco':
            bradesco_processor = RetornoBradescoProcessor()
            bradesco_processor.process_file(arquivo_retorno=self.arquivo_retorno.file)
        #if self.banco == 'itau':
        #    itau_processor = RetornoItauProcessor()
        #    itau_processor.process_file(arquivo_retorno=self.arquivo_retorno.file)

    
    def __unicode__(self):
        return '%s importado %s' % (self.arquivo_retorno.name, self.date_import) 

    class Meta:
        verbose_name = _('returnFile')
        verbose_name_plural = _('returnFiles')

reversion.register(ReturnFile)

