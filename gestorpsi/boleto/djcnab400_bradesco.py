# -*- coding: utf-8 -*-

from datetime import datetime
import httplib
import urllib
import urllib2
import re


from gestorpsi.boleto.models import *

def int_or_0(value):
    try:
        return int(value)
    except:
        return 0


def readHeader(header, ret):

    cont = ReturnFile.objects.filter(header_data_gravacao=datetime.strptime(header[95:101], "%d%m%y")).count()
    if cont > 0:
        return None
    del cont

    ret.header_registro           = int_or_0(header[1:2])   #9 Identificação do Registro Header: “0”
    ret.header_tipo_operacao      = int_or_0(header[2:3])   #9 Tipo de Operação: “2”
    ret.header_id_tipo_operacao   = int_or_0(header[3:10])   #X Identificação Tipo de Operação “RETORNO”
    ret.header_id_tipo_servico    = int_or_0(header[10:12])   #9 Identificação do Tipo de Serviço: “01”
    ret.header_tipo_servico       = int_or_0(header[12:27])   #X Identificação por Extenso do Tipo de Serviço: “COBRANCA”
    ret.header_cod_cliente        = int_or_0(header[27:47])
    ret.header_nome_cliente       = int_or_0(header[47:77])   #razao social
    ret.header_num_banco          = int_or_0(header[77:80])   #237 (Código do bradesco)
    ret.header_nome_empresa       = int_or_0(header[80:95])   #Nome do banco (BRADESCO)
    ret.header_data_gravacao      = datetime.strptime(header[95:101], "%d%m%y")#.strftime("%Y-%m-%d")   #9 Data da Gravação: Informe no formato “DDMMAA”
    ret.header_densidade_gravacao = int_or_0(header[101:109])   #01600000
    ret.header_num_aviso_bancario = int_or_0(header[109:114])
    ret.header_data_credito       = datetime.strptime(header[380:386], "%d%m%y")#.strftime("%Y-%m-%d")   # “DDMMAA”
    ret.header_sequencial_reg     = int_or_0(header[395:401])   #9 Seqüencial do Registro: ”000001”
    return ret

def readDetail(detail):
    det = DetailLine()
                                                      #X = ALFANUMÉRICO 9 = NUMÉRICO V = VÍRGULA DECIMAL ASSUMIDA
    det.detail_registro              = int_or_0(detail[1:2])        #9  Id do Registro Detalhe: 1
    det.detail_tipo_inscr_empresa    = int_or_0(detail[2:4])        #9  01-CPF | 02-CNPJ | 03-PIS/PASEP | 98-Não tem | 99-Outro
    det.detail_num_inscr_empresa     = detail[4:18]       #9  CNPJ/CPF, Número, Filial ou Controle
    det.detail_id_empresa_banco      = detail[21:48]      #9  Identificação da Empresa Cedente no Banco
                                                      #Zero, Carteira (size=3), Agência (size=5) e Conta Corrente (size=8)

    det.detail_num_controle_part     = int_or_0(detail[38:63])      #No Controle do Participante | Uso da Empresa
    det.detail_nosso_numero          = int_or_0(detail[71:83])      #Identificação do Título no Banco
    det.detail_id_rateio_credito     = int_or_0(detail[105:106])    #Indicador de Rateio Crédito “R”
    det.detail_carteira              = int_or_0(detail[108:109])    #Carteira
    det.detail_id_ocorrencia         = int_or_0(detail[109:110])    #Identificação de Ocorrência (vide pg 47)
    det.detail_data_ocorrencia       = datetime.strptime(detail[111:117], "%d%m%y")#.strftime("%Y-%m-%d")    #X  Data da Entrada/Liquidação (DDMMAA)
    det.detail_num_documento         = int_or_0(detail[117:127])    #A  Número título dado pelo cedente
    det.detail_id_titulo_banco       = int_or_0(detail[127:147])    #mesmo valor que o campo nosso_numero (indicado anteriormente)
    det.detail_data_vencimento       = datetime.strptime(detail[147:153], "%d%m%y")#.strftime("%Y-%m-%d")    #9  Data de vencimento (DDMMAA)
    det.detail_valor                 = int_or_0(detail[153:166])    #9  v99 Valor do título
    det.detail_cod_banco             = int_or_0(detail[166:169])    #9  Código do banco recebedor
    det.detail_agencia               = int_or_0(detail[169:174])    #9  Código da agência recebedora
    det.detail_desp_cobranca         = int_or_0(detail[176:189])    # Despesas de cobrança para
                                                        #os Códigos de Ocorrência
                                                        #02 - Entrada Confirmada
                                                        #28 - Débito de Tarifas
    
    det.detail_outras_despesas       = int_or_0(detail[189:202]) #9  v99 Outras despesas
    det.detail_juros_atraso          = int_or_0(detail[202:215]) #9  v99 Juros atraso
    det.detail_iof                   = int_or_0(detail[215:228]) #9  v99 IOF
    det.detail_valor_abatimento      = int_or_0(detail[228:241]) #9  v99 Valor do abatimento
    det.detail_desconto_concedido    = int_or_0(detail[241:254]) #9  v99 Desconto concedido
    det.detail_valor_recebido        = int_or_0(detail[254:267]) #9  v99 Valor pago
    det.detail_juros_mora            = int_or_0(detail[267:280]) #9  v99 Juros de mora
    det.detail_outros_recebimentos   = int_or_0(detail[280:293]) #9  v99 Outros recebimentos
    det.detail_abatimento_nao_aprov  = int_or_0(detail[293:306]) #9  v99 Abatimento não aproveitado pelo sacado
    det.detail_valor_lancamento      = int_or_0(detail[306:319]) #9  v99 Valor do lançamento
    det.detail_motivo_cod_ocorrencia = int_or_0(detail[319:329])  #Motivos das Rejeições para
                                                        #os Códigos de Ocorrência da Posição 109 a 110
    det.detail_indicativo_dc         = int_or_0(detail[319:320]) #9  Indicativo de débito/crédito - ver nota 11
    det.detail_indicador_valor       = int_or_0(detail[320:321]) #9  Indicador de valor -ver  nota 12
    det.detail_valor_ajuste          = int_or_0(detail[321:333]) #9  v99 Valor do ajuste - ver nota 13
    det.detail_num_cartorio          = int_or_0(detail[369:371])
    det.detail_num_protocolo         = int_or_0(detail[371:381])
    det.detail_sequencial            = int_or_0(detail[395:401]) #9 Seqüencial do registro

    return det


def readTrailer(trailer, ret):

    ret.trailer_registro                = int_or_0(trailer[1:2])  #9  Identificação do Registro Trailer: “9”
    ret.trailer_retorno                 = int_or_0(trailer[2:3])  #9  “2”
    ret.trailer_tipo_registro           = int_or_0(trailer[3:5])  #9  “01”
    ret.trailer_cod_banco               = int_or_0(trailer[5:8])
    ret.trailer_cob_simples_qtd_titulos = int_or_0(trailer[18:26])  #9  Cobrança Simples - quantidade de títulos em cobranca
    ret.trailer_cob_simples_vlr_total   = int_or_0(trailer[26:40]) #9  v99 Cobrança Simples - valor total
    ret.trailer_cob_simples_num_aviso   = int_or_0(trailer[40:48])  #9  Cobrança Simples - Número do aviso
    ret.trailer_qtd_regs02              = int_or_0(trailer[58:63])  #Quantidade  de Registros- Ocorrência 02 – Confirmação de Entradas
    ret.trailer_valor_regs02            = int_or_0(trailer[63:75]) #Valor dos Registros- Ocorrência 02 – Confirmação de Entradas
    ret.trailer_valor_regs06liq         = int_or_0(trailer[75:87]) #Valor dos Registros- Ocorrência 06 liquidacao
    ret.trailer_qtd_regs06              = int_or_0(trailer[87:92])  #Quantidade  de Registros- Ocorrência 06 – liquidacao
    ret.trailer_valor_regs06            = int_or_0(trailer[92:104]) #Valor dos Registros- Ocorrência 06
    ret.trailer_qtd_regs09              = int_or_0(trailer[104:109])  #Quantidade  de Registros- Ocorrência 09 e 10
    ret.trailer_valor_regs02            = int_or_0(trailer[109:121]) #Valor dos  Registros- Ocorrência 09 e 10
    ret.trailer_qtd_regs13              = int_or_0(trailer[121:126])  #Quantidade  de Registros- Ocorrência 13
    ret.trailer_valor_regs13            = int_or_0(trailer[126:138]) #Valor dos  Registros- Ocorrência 13
    ret.trailer_qtd_regs14              = int_or_0(trailer[138:143])  #Quantidade  de Registros- Ocorrência 14
    ret.trailer_valor_regs14            = int_or_0(trailer[143:155]) #Valor dos  Registros- Ocorrência 14
    ret.trailer_qtd_regs12              = int_or_0(trailer[155:160])  #Quantidade  de Registros- Ocorrência 12
    ret.trailer_valor_regs12            = int_or_0(trailer[160:172]) #Valor dos  Registros- Ocorrência 12
    ret.trailer_qtd_regs19              = int_or_0(trailer[172:177])  #Quantidade  de Registros- Ocorrência 19
    ret.trailer_valor_regs19            = int_or_0(trailer[177:189]) #Valor dos  Registros- Ocorrência 19
    ret.trailer_valor_total_rateios     = int_or_0(trailer[363:378])
    ret.trailer_qtd_rateios             = int_or_0(trailer[378:386])
    ret.trailer_sequencial              = int_or_0(trailer[395:401])  #9  Seqüencial do registro

    return ret


def cnab400(file):
    #file = open("/home/jayme/Desktop/doois/gestorpsi/retorno-cb030400-bradesco.ret", 'r+')

    ret = ReturnFile()
    header = ""
    trailer = ""
    lines = []

    while True:
        line = file.readline()
        if line == "":
            break
        if line[0] == '0': #header
            ret = readHeader(" "+line, ret)
            if ret is None:
                break
        elif line[0] == '1': #detail
            lines.append( readDetail(" "+line) )
        elif line[0] == '9': #trailer
            ret = readTrailer(" "+line, ret)
    file.close()
    
    if ret is not None:
        ret.save()
        for p in lines:
            p.file = ret
            p.save()
    
    return ret

if __name__ == "__main__":
    cnab400()

