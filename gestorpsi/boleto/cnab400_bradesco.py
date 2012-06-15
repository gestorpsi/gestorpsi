# -*- coding: utf-8 -*-

import datetime
import httplib
import urllib
import urllib2
import re

#from collections import OrderedDict - python 2.7+

'''
from django.utils.encoding import smart_str, force_unicode
from gestorpsi.boleto.models import BradescoBilletData
from django.contrib.auth.models import User
from gestorpsi.document.models import Document, TypeDocument
from gestorpsi.address.models import City, Address, Country
'''

def readHeader(header):
    head = {}

    head["registro"]           = header[1:2]   #9 Identificação do Registro Header: “0”
    head["tipo_operacao"]      = header[2:3]   #9 Tipo de Operação: “2”
    head["id_tipo_operacao"]   = header[3:10]   #X Identificação Tipo de Operação “RETORNO”
    head["id_tipo_servico"]    = header[10:12]   #9 Identificação do Tipo de Serviço: “01”
    head["tipo_servico"]       = header[12:27]   #X Identificação por Extenso do Tipo de Serviço: “COBRANCA”
    head["cod_cliente"]        = header[27:47]
    head["nome_cliente"]       = header[47:77]   #razao social
    head["num_banco"]          = header[77:80]   #237 (Código do bradesco)
    head["nome_empresa"]       = header[80:95]   #Nome do banco (BRADESCO)
    head["data_gravacao"]      = header[95:101]   #9 Data da Gravação: Informe no formato “DDMMAA”
    head["densidade_gravacao"] = header[101:109]   #01600000
    head["num_aviso_bancario"] = header[109:114]
    head["data_credito"]       = header[380:386]   # “DDMMAA”
    head["sequencial_reg"]     = header[395:401]   #9 Seqüencial do Registro: ”000001”
    return head

def readDetail(detail):
    det = {}
                                                      #X = ALFANUMÉRICO 9 = NUMÉRICO V = VÍRGULA DECIMAL ASSUMIDA
    det["registro"]              = detail[1:2]        #9  Id do Registro Detalhe: 1
    det["tipo_inscr_empresa"]    = detail[2:4]        #9  01-CPF | 02-CNPJ | 03-PIS/PASEP | 98-Não tem | 99-Outro
    det["num_inscr_empresa"]     = detail[4:18]       #9  CNPJ/CPF, Número, Filial ou Controle
    det["id_empresa_banco"]      = detail[21:48]      #9  Identificação da Empresa Cedente no Banco
                                                      #Zero, Carteira (size=3), Agência (size=5) e Conta Corrente (size=8)

    det["num_controle_part"]     = detail[38:63]      #No Controle do Participante | Uso da Empresa
    det["nosso_numero"]          = detail[71:83]      #Identificação do Título no Banco
    det["id_rateio_credito"]     = detail[105:106]    #Indicador de Rateio Crédito “R”
    det["carteira"]              = detail[108:109]    #Carteira
    det["id_ocorrencia"]         = detail[109:110]    #Identificação de Ocorrência (vide pg 47)
    det["data_ocorrencia"]       = detail[111:117]    #X  Data da Entrada/Liquidação (DDMMAA)
    det["num_documento"]         = detail[117:127]    #A  Número título dado pelo cedente
    det["id_titulo_banco"]       = detail[127:147]    #mesmo valor que o campo nosso_numero (indicado anteriormente)
    det["data_vencimento"]       = detail[147:153]    #9  Data de vencimento (DDMMAA)
    det["valor"]                 = detail[153:166]    #9  v99 Valor do título
    det["cod_banco"]             = detail[166:169]    #9  Código do banco recebedor
    det["agencia"]               = detail[169:174]    #9  Código da agência recebedora
    det["desp_cobranca"]         = detail[176:189]    # Despesas de cobrança para
                                                        #os Códigos de Ocorrência
                                                        #02 - Entrada Confirmada
                                                        #28 - Débito de Tarifas
    
    det["outras_despesas"]       = detail[189:202] #9  v99 Outras despesas
    det["juros_atraso"]          = detail[202:215] #9  v99 Juros atraso
    det["iof"]                   = detail[215:228] #9  v99 IOF
    det["valor_abatimento"]      = detail[228:241] #9  v99 Valor do abatimento
    det["desconto_concedido"]    = detail[241:254] #9  v99 Desconto concedido
    det["valor_recebido"]        = detail[254:267] #9  v99 Valor pago
    det["juros_mora"]            = detail[267:280] #9  v99 Juros de mora
    det["outros_recebimentos"]   = detail[280:293] #9  v99 Outros recebimentos
    det["abatimento_nao_aprov"]  = detail[293:306] #9  v99 Abatimento não aproveitado pelo sacado
    det["valor_lancamento"]      = detail[306:319] #9  v99 Valor do lançamento
    det["motivo_cod_ocorrencia"] = detail[319:329]  #Motivos das Rejeições para
                                                        #os Códigos de Ocorrência da Posição 109 a 110
    det["indicativo_dc"]         = detail[319:320] #9  Indicativo de débito/crédito - ver nota 11
    det["indicador_valor"]       = detail[320:321] #9  Indicador de valor -ver  nota 12
    det["valor_ajuste"]          = detail[321:333] #9  v99 Valor do ajuste - ver nota 13
    det["num_cartorio"]          = detail[369:371]
    det["num_protocolo"]         = detail[371:381]
    det["sequencial"]            = detail[395:401] #9 Seqüencial do registro

    return det


def readTrailer(trailer):
    trail = {}
    
    trail["registro"]                = trailer[1:2]  #9  Identificação do Registro Trailer: “9”
    trail["retorno"]                 = trailer[2:3]  #9  “2”
    trail["tipo_registro"]           = trailer[3:5]  #9  “01”
    trail["cod_banco"]               = trailer[5:8]
    trail["cob_simples_qtd_titulos"] = trailer[18:26]  #9  Cobrança Simples - quantidade de títulos em cobranca
    trail["cob_simples_vlr_total"]   = trailer[26:40] #9  v99 Cobrança Simples - valor total
    trail["cob_simples_num_aviso"]   = trailer[40:48]  #9  Cobrança Simples - Número do aviso
    trail["qtd_regs02"]              = trailer[58:63]  #Quantidade  de Registros- Ocorrência 02 – Confirmação de Entradas
    trail["valor_regs02"]            = trailer[63:75] #Valor dos Registros- Ocorrência 02 – Confirmação de Entradas
    trail["valor_regs06liq"]         = trailer[75:87] #Valor dos Registros- Ocorrência 06 liquidacao
    trail["qtd_regs06"]              = trailer[87:92]  #Quantidade  de Registros- Ocorrência 06 – liquidacao
    trail["valor_regs06"]            = trailer[92:104] #Valor dos Registros- Ocorrência 06
    trail["qtd_regs09"]              = trailer[104:109]  #Quantidade  de Registros- Ocorrência 09 e 10
    trail["valor_regs02"]            = trailer[109:121] #Valor dos  Registros- Ocorrência 09 e 10
    trail["qtd_regs13"]              = trailer[121:126]  #Quantidade  de Registros- Ocorrência 13
    trail["valor_regs13"]            = trailer[126:138] #Valor dos  Registros- Ocorrência 13
    trail["qtd_regs14"]              = trailer[138:143]  #Quantidade  de Registros- Ocorrência 14
    trail["valor_regs14"]            = trailer[143:155] #Valor dos  Registros- Ocorrência 14
    trail["qtd_regs12"]              = trailer[155:160]  #Quantidade  de Registros- Ocorrência 12
    trail["valor_regs12"]            = trailer[160:172] #Valor dos  Registros- Ocorrência 12
    trail["qtd_regs19"]              = trailer[172:177]  #Quantidade  de Registros- Ocorrência 19
    trail["valor_regs19"]            = trailer[177:189] #Valor dos  Registros- Ocorrência 19
    trail["valor_total_rateios"]     = trailer[363:378]
    trail["qtd_rateios"]             = trailer[378:386]
    trail["sequencial"]              = trailer[395:401]  #9  Seqüencial do registro

    return trail


def cnab400():
    file = open("/home/jayme/Desktop/doois/gestorpsi/retorno-cb030400-bradesco.ret", 'r+')

    header = ""
    trailer = ""
    lines = []

    while True:
        line = file.readline()
        if line == "":
            break
        if line[0] == '0': #header
            header = readHeader(" "+line)
        elif line[0] == '1': #detail
            lines.append( readDetail(" "+line) )
        elif line[0] == '9': #trailer
            trailer = readTrailer(" "+line)
    file.close()
    

if __name__ == "__main__":
    cnab400()

