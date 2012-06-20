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
from django.utils.encoding import smart_str


class BradescoBilletData(models.Model):
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

    contabancaria_numerodaconta = models.CharField(max_length=7, null=True, blank=True)
    contabancaria_numerodaconta.widget = forms.TextInput(attrs={"mask": "999999",})
    contabancaria_numerodaconta.verbose_name = _("Account")
    contabancaria_numerodaconta.help_text = _("Number of the bank account of the seller.")
    contabancaria_numerodaconta_digito = models.CharField(max_length=1, null=True, blank=True)
    contabancaria_numerodaconta_digito.widget = forms.TextInput(attrs={"mask": "9",})
    contabancaria_numerodaconta_digito.verbose_name = _("Verifier digit")
    contabancaria_numerodaconta_digito.help_text = _("Verifier digit of the bank account of the seller.")
    contabancaria_carteira = models.PositiveIntegerField(null=True, blank=True, validators=[MaxValueValidator(99)])
    contabancaria_carteira.verbose_name = _("Seller's wallet")
    contabancaria_carteira.help_text = _("Seller's bank wallet number")
    contabancaria_agencia = models.CharField(max_length=255, null=True, blank=True)
    contabancaria_agencia.widget = forms.TextInput(attrs={"mask": "9999",})
    contabancaria_agencia.verbose_name = _("Agency")
    contabancaria_agencia.help_text = _("Seller's account agency")
    contabancaria_agencia_digito = models.CharField(max_length=1, null=True, blank=True)
    contabancaria_agencia_digito.widget = forms.TextInput(attrs={"mask": "9",})
    contabancaria_agencia_digito.verbose_name = _("Agency digit")
    contabancaria_agencia_digito.help_text = _("Seller's account agency verifier digit")


    titulo_nossonumero = models.CharField(max_length=11, null=True, blank=True, validators=[MinLengthValidator(11)])
    titulo_nossonumero.verbose_name = _("\"Our number\"")
    titulo_nossonumero.help_text = _("Number registered in Bradesco to register the receiving of billets.")
    
    titulo_digitodonossonumero = models.CharField(max_length=1, null=True, blank=True)
    titulo_digitodonossonumero.widget = forms.TextInput(attrs={"mask": "9",})
    titulo_digitodonossonumero.verbose_name = _("\"Our number\" digit")
    titulo_digitodonossonumero.help_text = _("\"Our number\" digit")


    def __unicode__(self):
        return smart_str(self.cedente_nome)


reversion.register(BradescoBilletData)





class NullManager(models.Manager):
    def get_for_model(self, model):
        return None


class ReturnFile(models.Model):
    #objects = NullManager()
    
    ############   start: header of the return file   ############
    header_registro = models.IntegerField(null=True, blank=True)   #9 Identificação do Registro Header: “0”
    header_tipo_operacao = models.IntegerField(null=True, blank=True)   #9 Tipo de Operação: “2”
    header_id_tipo_operacao = models.CharField(max_length=7, null=True, blank=True)   #X Identificação Tipo de Operação “RETORNO”
    header_id_tipo_servico = models.IntegerField(null=True, blank=True)   #9 Identificação do Tipo de Serviço: “01”
    header_tipo_servico = models.CharField(max_length=15, null=True, blank=True)   #X Identificação por Extenso do Tipo de Serviço: “COBRANCA”
    header_cod_cliente = models.IntegerField(null=True, blank=True)
    header_nome_cliente = models.CharField(max_length=30, null=True, blank=True)   #razao social
    header_num_banco = models.IntegerField(null=True, blank=True)  #237 (Código do bradesco)
    header_nome_empresa = models.CharField(max_length=15, null=True, blank=True)   #Nome do banco (BRADESCO)
    header_data_gravacao = models.DateField(null=True, blank=True, unique=True)   #9 Data da Gravação: Informe no formato “DDMMAA”
    header_densidade_gravacao = models.IntegerField(null=True, blank=True)   #01600000
    header_num_aviso_bancario = models.IntegerField(null=True, blank=True, unique=True)
    #header_num_aviso_bancario.verbose_name = ""
    #header_num_aviso_bancario.help_text = ""
    header_data_credito = models.DateField(null=True, blank=True)   # “DDMMAA”
    header_sequencial_reg = models.IntegerField(null=True, blank=True)   #9 Seqüencial do Registro: ”000001”
    ############   end: header of the return file   ############
    
    ############   start: trailer of the return file   ############
    trailer_registro = models.IntegerField(null=True, blank=True)  #9  Identificação do Registro Trailer: “9”
    trailer_retorno = models.IntegerField(null=True, blank=True)  #9  “2”
    trailer_tipo_registro = models.IntegerField(null=True, blank=True)  #9  “01”
    trailer_cod_banco = models.IntegerField(null=True, blank=True)
    trailer_cob_simples_qtd_titulos = models.IntegerField(null=True, blank=True)  #9  Cobrança Simples - quantidade de títulos em cobranca
    trailer_cob_simples_vlr_total = models.IntegerField(null=True, blank=True) #9  v99 Cobrança Simples - valor total
    trailer_cob_simples_num_aviso = models.IntegerField(null=True, blank=True)  #9  Cobrança Simples - Número do aviso
    trailer_qtd_regs02 = models.IntegerField(null=True, blank=True)  #Quantidade  de Registros- Ocorrência 02 – Confirmação de Entradas
    trailer_valor_regs02 = models.IntegerField(null=True, blank=True) #Valor dos Registros- Ocorrência 02 – Confirmação de Entradas
    trailer_valor_regs06liq = models.IntegerField(null=True, blank=True) #Valor dos Registros- Ocorrência 06 liquidacao
    trailer_qtd_regs06 = models.IntegerField(null=True, blank=True)  #Quantidade  de Registros- Ocorrência 06 – liquidacao
    trailer_valor_regs06 = models.IntegerField(null=True, blank=True) #Valor dos Registros- Ocorrência 06
    trailer_qtd_regs09 = models.IntegerField(null=True, blank=True)  #Quantidade  de Registros- Ocorrência 09 e 10
    trailer_valor_regs02 = models.IntegerField(null=True, blank=True) #Valor dos  Registros- Ocorrência 09 e 10
    trailer_qtd_regs13 = models.IntegerField(null=True, blank=True)  #Quantidade  de Registros- Ocorrência 13
    trailer_valor_regs13 = models.IntegerField(null=True, blank=True) #Valor dos  Registros- Ocorrência 13
    trailer_qtd_regs14 = models.IntegerField(null=True, blank=True)  #Quantidade  de Registros- Ocorrência 14
    trailer_valor_regs14 = models.IntegerField(null=True, blank=True) #Valor dos  Registros- Ocorrência 14
    trailer_qtd_regs12 = models.IntegerField(null=True, blank=True)  #Quantidade  de Registros- Ocorrência 12
    trailer_valor_regs12 = models.IntegerField(null=True, blank=True) #Valor dos  Registros- Ocorrência 12
    trailer_qtd_regs19 = models.IntegerField(null=True, blank=True)  #Quantidade  de Registros- Ocorrência 19
    trailer_valor_regs19 = models.IntegerField(null=True, blank=True) #Valor dos  Registros- Ocorrência 19
    trailer_valor_total_rateios = models.IntegerField(null=True, blank=True)
    trailer_qtd_rateios = models.IntegerField(null=True, blank=True)
    trailer_sequencial = models.IntegerField(null=True, blank=True)  #9  Seqüencial do registro
    ############   end: trailer of the return file   ############

    def __unicode__(self):
        return smart_str(self.header_data_gravacao.strftime("%d/%m/%Y"))

    def __str__(self):
        return smart_str(self.header_data_gravacao.strftime("%d/%m/%Y"))

    def save(self):
        super(ReturnFile, self).save()

reversion.register(ReturnFile)



class DetailLine(models.Model):
    detail_registro = models.IntegerField(null=True, blank=True)        #9  Id do Registro Detalhe: 1
    detail_tipo_inscr_empresa = models.IntegerField(null=True, blank=True)        #9  01-CPF | 02-CNPJ | 03-PIS/PASEP | 98-Não tem | 99-Outro
    detail_num_inscr_empresa = models.CharField(max_length=15, null=True, blank=True)       #9  CNPJ/CPF, Número, Filial ou Controle
    detail_id_empresa_banco = models.CharField(max_length=28, null=True, blank=True)      #9  Identificação da Empresa Cedente no Banco
                                                      #Zero, Carteira (size=3), Agência (size=5) e Conta Corrente (size=8)

    detail_num_controle_part = models.IntegerField(null=True, blank=True)      #No Controle do Participante | Uso da Empresa
    detail_nosso_numero = models.IntegerField(null=True, blank=True)      #Identificação do Título no Banco
    detail_id_rateio_credito = models.IntegerField(null=True, blank=True)    #Indicador de Rateio Crédito “R”
    detail_carteira = models.IntegerField(null=True, blank=True)    #Carteira
    detail_id_ocorrencia = models.IntegerField(null=True, blank=True)    #Identificação de Ocorrência (vide pg 47)
    detail_data_ocorrencia = models.DateField(null=True, blank=True, unique=True)    #X  Data da Entrada/Liquidação (DDMMAA)
    detail_num_documento = models.IntegerField(null=True, blank=True)    #A  Número título dado pelo cedente
    detail_id_titulo_banco = models.IntegerField(null=True, blank=True)    #mesmo valor que o campo nosso_numero (indicado anteriormente)
    detail_data_vencimento = models.DateField(null=True, blank=True)    #9  Data de vencimento (DDMMAA)
    detail_valor = models.IntegerField(null=True, blank=True)    #9  v99 Valor do título
    detail_cod_banco = models.IntegerField(null=True, blank=True)    #9  Código do banco recebedor
    detail_agencia = models.IntegerField(null=True, blank=True)    #9  Código da agência recebedora
    detail_desp_cobranca = models.IntegerField(null=True, blank=True)    # Despesas de cobrança para
                                                        #os Códigos de Ocorrência
                                                        #02 - Entrada Confirmada
                                                        #28 - Débito de Tarifas
    
    detail_outras_despesas = models.IntegerField(null=True, blank=True) #9  v99 Outras despesas
    detail_juros_atraso = models.IntegerField(null=True, blank=True) #9  v99 Juros atraso
    detail_iof = models.IntegerField(null=True, blank=True) #9  v99 IOF
    detail_valor_abatimento = models.IntegerField(null=True, blank=True) #9  v99 Valor do abatimento
    detail_desconto_concedido = models.IntegerField(null=True, blank=True) #9  v99 Desconto concedido
    detail_valor_recebido = models.IntegerField(null=True, blank=True) #9  v99 Valor pago
    detail_juros_mora = models.IntegerField(null=True, blank=True) #9  v99 Juros de mora
    detail_outros_recebimentos = models.IntegerField(null=True, blank=True) #9  v99 Outros recebimentos
    detail_abatimento_nao_aprov = models.IntegerField(null=True, blank=True) #9  v99 Abatimento não aproveitado pelo sacado
    detail_valor_lancamento = models.IntegerField(null=True, blank=True) #9  v99 Valor do lançamento
    detail_motivo_cod_ocorrencia = models.IntegerField(null=True, blank=True)  #Motivos das Rejeições para
                                                        #os Códigos de Ocorrência da Posição 109 a 110
    detail_indicativo_dc = models.IntegerField(null=True, blank=True) #9  Indicativo de débito/crédito - ver nota 11
    detail_indicador_valor = models.IntegerField(null=True, blank=True) #9  Indicador de valor -ver  nota 12
    detail_valor_ajuste = models.IntegerField(null=True, blank=True) #9  v99 Valor do ajuste - ver nota 13
    detail_num_cartorio = models.IntegerField(null=True, blank=True)
    detail_num_protocolo = models.IntegerField(null=True, blank=True)
    detail_sequencial = models.IntegerField(null=True, blank=True) #9 Seqüencial do registro

    file = models.ForeignKey(ReturnFile, null=True, blank=True)
    
    def __unicode__(self):
        return smart_str(self.detail_data_ocorrencia)

    def save(self):
        super(DetailLine, self).save()

reversion.register(DetailLine)

