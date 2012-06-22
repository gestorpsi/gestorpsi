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

from django.contrib import admin
from django.core.validators import BaseValidator, MinLengthValidator, MaxValueValidator
from django.core import exceptions
from django.utils.encoding import smart_str
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django import forms
from django.forms.models import *
from django.forms import *

from django.db import models
from django.utils.translation import ugettext as _

from smart_selects.db_fields import ChainedForeignKey

from gestorpsi import settings
from gestorpsi.address.models import State, City
from gestorpsi.boleto.models import BradescoBilletData
from gestorpsi.boleto.return_file import *


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
    cedente_nome.verbose_name = _("Seller's name")
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
              settings.MEDIA_URL+"js/jquery.maskedinput-1.1.3.admin.js",
              settings.MEDIA_URL+"js/boleto.admin.js",
        )
        css = {
              "all": (settings.MEDIA_URL+"css/boleto.admin.css", )
        }




class BradescoBilletDataAdmin(admin.ModelAdmin):
    model = BradescoBilletData

        
    form = BradescoBilletDataAdminForm
    actions = None

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    #view para listagem de objetos deste tipo
    def changelist_view(self, request, extra_context=None, **kwargs):
        c = BradescoBilletData.objects.all()[0]
        return HttpResponseRedirect( reverse('admin:boleto_bradescobilletdata_change', args=(c.id,)) )

    fieldsets = (
        ( _('Seller'), {
            'fields': ('cedente_nome', 'cedente_cnpj')
        }),
        ( _('Guarantor'), {
            'fields': ('sacadoravalista_nome', 'sacadoravalista_cnpj', 'enderecosacaval_uf',
                       'enderecosacaval_localidade', 'enderecosacaval_cep', 'enderecosacaval_bairro', 
                       'enderecosacaval_logradouro', 'enderecosacaval_numero')
        }),
        ( _('Bank account'), {
            'fields': ('contabancaria_numerodaconta', 'contabancaria_numerodaconta_digito', 
                       'contabancaria_carteira', 'contabancaria_agencia', 'contabancaria_agencia_digito')
        }),
        ( _('Title'), {
            'fields': ('titulo_nossonumero', 'titulo_digitodonossonumero')
        }),
    )

    #formfield_overrides = {
    #    models.TextField: {'widget': RichTextEditorWidget},
    #}

'''
class DetailLineInlineForm(forms.ModelForm):
   
    class Meta:
        model = DetailLine
        #fields = ()
    #def to_python(self):
    #    pass
    #def validate(self):
    #    pass
    #def save(self, request, *args, **kwargs):
    #    pass

class DetailLineInline(admin.StackedInline):
    model = DetailLine
    form = DetailLineInlineForm
    extra = 0


class ReturnFileAdminForm(forms.ModelForm):
    arquivo_retorno = forms.FileField(required=False)
    arquivo_retorno.help_text = "Quack"
    arquivo_retorno.label = "Arquivo de retorno do banco"
    
    class Meta:
        model = ReturnFile
        #exclude = ('header_registro', 'header_tipo_operacao', 'header_id_tipo_operacao', 'header_id_tipo_servico', 
        #           'header_tipo_servico', 'header_cod_cliente', 'header_nome_cliente', 'header_num_banco', 'header_nome_empresa', 
        #           'header_data_gravacao', 'header_densidade_gravacao', 'header_num_aviso_bancario', 'header_data_credito', 
        #           'header_sequencial_reg', 'trailer_registro', 'trailer_retorno', 'trailer_tipo_registro', 'trailer_cod_banco', 
        #           'trailer_cob_simples_qtd_titulos', 'trailer_cob_simples_vlr_total', 'trailer_cob_simples_num_aviso', 'trailer_qtd_regs02', 
        #           'trailer_valor_regs02', 'trailer_valor_regs06liq', 'trailer_qtd_regs06', 'trailer_valor_regs06', 'trailer_qtd_regs09', 
        #           'trailer_valor_regs02', 'trailer_qtd_regs13', 'trailer_valor_regs13', 'trailer_qtd_regs14', 'trailer_valor_regs14', 
        #           'trailer_qtd_regs12', 'trailer_valor_regs12', 'trailer_qtd_regs19', 'trailer_valor_regs19', 'trailer_valor_total_rateios', 
        #           'trailer_qtd_rateios', 'trailer_sequencial')
    def save(self, commit=True):  
        if self.instance.pk is None:
            fail_message = 'created'
            
            from gestorpsi.boleto.djcnab400_bradesco import cnab400
            import StringIO
            temp = StringIO.StringIO(self.cleaned_data['arquivo_retorno'].read())
            #cnab400(temp)
            #raise Exception( self )
            ret = cnab400(temp)
            if ret is None:
                for p in ReturnFile.objects.all():
                    for k in DetailLine.objects.all():
                        k.delete()
                    p.delete()
                raise Exception('teste')
                return save_instance(self, self.instance, self._meta.fields, fail_message, commit, construct=False)
            else:
                self.instance = ret
                #raise Exception('teste2')
                return save_instance(self, self.instance, self._meta.fields, fail_message, commit, construct=False)
        else:
            fail_message = 'changed'
            return save_instance(self, self.instance, self._meta.fields, fail_message, commit, construct=False)
    #def save(self, commit=False):
    #    from gestorpsi.boleto.djcnab400_bradesco import cnab400
    #    import StringIO
    #    temp = StringIO.StringIO(self.cleaned_data['arquivo_retorno'].read())
    #    #cnab400(temp)
    #    #raise Exception( temp.readline()[108:112] )
    #    ret = cnab400(temp)
    #    if ret is None:
    #        for p in ReturnFile.objects.all():
    #            for k in DetailLine.objects.all():
    #                k.delete()
    #            p.delete()
    #    #else:
    #    #    raise Exception(ret.header_data_credito)
    #    super(ReturnFileAdminForm, self).save(commit)'''

      
class ReturnFileAdmin(admin.ModelAdmin):
    #inlines = [DetailLineInline, ]
    #form = ReturnFileAdminForm
    pass
    #def save_model(self, request, obj, form, change):
    #    #raise Exception(obj)
    #    obj.save()


admin.site.register(BradescoBilletData, BradescoBilletDataAdmin)
admin.site.register(ReturnFile, ReturnFileAdmin)
