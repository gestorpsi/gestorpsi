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
    aux = ''
    p = head["registro"]           = header[1:2]   #9 Identificação do Registro Header: “0”
    aux += p
    p = head["tipo_operacao"]      = header[2:3]   #9 Tipo de Operação: “2”
    aux += p
    p = head["id_tipo_operacao"]   = header[3:10]   #X Identificação Tipo de Operação “RETORNO”
    aux += p
    p = head["id_tipo_servico"]    = header[10:12]   #9 Identificação do Tipo de Serviço: “01”
    aux += p
    p = head["tipo_servico"]       = header[12:27]   #X Identificação por Extenso do Tipo de Serviço: “COBRANCA”
    aux += p
    p = head["cod_empresa"]        = header[27:47]
    aux += p
    p = head["nome_empresa"]       = header[47:77]   #razao social
    aux += p
    p = head["num_banco"]          = header[77:80]   #237 (Código do bradesco)
    aux += p
    p = head["banco"]              = header[80:95]   #Nome do banco (BRADESCO)
    aux += p
    p = head["data_gravacao"]      = header[95:101]   #9 Data da Gravação: Informe no formado “DDMMAA”
    aux += p
    p = head["densidade_gravacao"] = header[101:109]   #01600000
    aux += p
    p = head["num_aviso_bancario"] = header[109:114]
    aux += p
    p = head["data_credito"]       = header[380:386]   # “DDMMAA”
    aux += p
    p = head["sequencial_reg"]     = header[395:401]   #9 Seqüencial do Registro: ”000001”
    aux += p
    return head

def readDetail(detail):
    det = {}
    aux = ''

                                                        #X = ALFANUMÉRICO 9 = NUMÉRICO V = VÍRGULA DECIMAL ASSUMIDA
    p = det["registro"]            = detail[1:2]        #9  Id do Registro Detalhe: 1
    aux += p
    p = det["tipo_inscr_empresa"]  = detail[2:4]        #9  01-CPF | 02-CNPJ | 03-PIS/PASEP | 98-Não tem | 99-Outro
    aux += p
    p = det["num_inscr_empresa"]   = detail[4:18]       #9  CNPJ/CPF, Número, Filial ou Controle
    aux += p
    p = det["id_empresa_banco"]    = detail[21:48]      #9  Identificação da Empresa Cedente no Banco
                                                        #Zero, Carteira (size=3), Agência (size=5) e Conta Corrente (size=8)
    
    aux += p
    aux += p
    p = det["num_controle_part"]   = detail[38:63]      #No Controle do Participante | Uso da Empresa
    aux += p
    p = det["nosso_numero"]        = detail[71:83]      #Identificação do Título no Banco
    aux += p
    p = det["id_rateio_credito"]   = detail[105:106]    #Indicador de Rateio Crédito “R”
    aux += p
    p = det["carteira"]            = detail[108:109]    #Carteira
    aux += p
    p = det["id_ocorrencia"]       = detail[109:110]    #Identificação de Ocorrência (vide pg 47)
    aux += p
    p = det["data_ocorrencia"]     = detail[111:117]    #X  Data da Entrada/Liquidação (DDMMAA)
    aux += p
    p = det["num_documento"]       = detail[117:127]    #A  Número título dado pelo cedente
    aux += p
    p = det["id_titulo_banco"]     = detail[127:147]    #mesmo valor que o campo nosso_numero (indicado anteriormente)
    aux += p
    p = det["data_vencimento"]     = detail[147:153]    #9  Data de vencimento (DDMMAA)
    aux += p
    p = det["valor"]               = detail[153:166]    #9  v99 Valor do título
    aux += p
    p = det["cod_banco"]           = detail[166:169]    #9  Código do banco recebedor
    aux += p
    p = det["agencia"]             = detail[169:174]    #9  Código da agência recebedora
    aux += p
    p = det["desp_cobranca"]       = detail[176:189]    # Despesas de cobrança para
                                                        #os Códigos de Ocorrência
                                                        #02 - Entrada Confirmada
                                                        #28 - Débito de Tarifas
    
    aux += p
    p = det["outras_despesas"]     = detail[189:202] #9  v99 Outras despesas
    aux += p
    p = det["juros_atraso"]        = detail[202:215] #9  v99 Juros atraso
    aux += p
    p = det["iof"]                 = detail[215:228] #9  v99 IOF
    aux += p
    p = det["valor_abatimento"]    = detail[228:241] #9  v99 Valor do abatimento
    aux += p
    p = det["desconto_concedido"]  = detail[241:254] #9  v99 Desconto concedido
    aux += p
    p = det["valor_recebido"]      = detail[254:267] #9  v99 Valor pago
    aux += p
    p = det["juros_mora"]          = detail[267:280] #9  v99 Juros de mora
    aux += p
    p = det["outros_recebimentos"] = detail[280:293] #9  v99 Outros recebimentos
    aux += p
    p = det["abatimento_nao_aprov"]= detail[293:306] #9  v99 Abatimento não aproveitado pelo sacado
    aux += p
    p = det["valor_lancamento"]    = detail[306:319] #9  v99 Valor do lançamento
    aux += p
    p = det["motivo_cod_ocorrencia"] = detail[319:329]  #Motivos das Rejeições para
                                                        #os Códigos de Ocorrência da Posição 109 a 110
    aux += p
    p = det["indicativo_dc"]       = detail[319:320] #9  Indicativo de débito/crédito - ver nota 11
    aux += p
    p = det["indicador_valor"]     = detail[320:321] #9  Indicador de valor -ver  nota 12
    aux += p
    p = det["valor_ajuste"]        = detail[321:333] #9  v99 Valor do ajuste - ver nota 13
    aux += p
    p = det["num_cartorio"] = detail[369:371]
    aux += p
    p = det["num_protocolo"] = detail[371:381]
    aux += p
    p = det["sequencial"]          = detail[395:401] #9 Seqüencial do registro
    aux += p

    return det

#sendo feito
def readTrailer(trailer):
    trail = {}
    aux = ''
    p = head["registro"]           = header[1:2]   #9 Identificação do Registro Header: “0”
    aux += p

    
    trail["registro"]                = trailer[1:2]  #9  Identificação do Registro Trailer: “9”
    trail["retorno"]                 = trailer[2:3]  #9  “2”
    trail["tipo_registro"]           = trailer[3:5]  #9  “01”
    trail["cod_banco"]               = trailer[5:8]
    trail["cob_simples_qtd_titulos"] = trailer[18:26]  #9  Cobrança Simples - quantidade de títulos em cobranca
    trail["cob_simples_vlr_total"]   = trailer[26,  14] #9  v99 Cobrança Simples - valor total
    trail["cob_simples_num_aviso"]   = trailer[40,   8]  #9  Cobrança Simples - Número do aviso
    trail["qtd_regs02"]              = trailer[58,   5]  #Quantidade  de Registros- Ocorrência 02 – Confirmação de Entradas
    trail["valor_regs02"]            = trailer[63,  12] #Valor dos Registros- Ocorrência 02 – Confirmação de Entradas
    trail["valor_regs06liq"]         = trailer[75,  12] #Valor dos Registros- Ocorrência 06 liquidacao
    trail["qtd_regs06"]              = trailer[87,   5]  #Quantidade  de Registros- Ocorrência 06 – liquidacao
    trail["valor_regs06"]            = trailer[92,  12] #Valor dos Registros- Ocorrência 06
    trail["qtd_regs09"]              = trailer[104,   5]  #Quantidade  de Registros- Ocorrência 09 e 10
    trail["valor_regs02"]            = trailer[109,  12] #Valor dos  Registros- Ocorrência 09 e 10
    trail["qtd_regs13"]              = trailer[121,   5]  #Quantidade  de Registros- Ocorrência 13
    trail["valor_regs13"]            = trailer[126,  12] #Valor dos  Registros- Ocorrência 13
    trail["qtd_regs14"]              = trailer[138,   5]  #Quantidade  de Registros- Ocorrência 14
    trail["valor_regs14"]            = trailer[143,  12] #Valor dos  Registros- Ocorrência 14
    trail["qtd_regs12"]              = trailer[155,   5]  #Quantidade  de Registros- Ocorrência 12
    trail["valor_regs12"]            = trailer[160,  12] #Valor dos  Registros- Ocorrência 12
    trail["qtd_regs19"]              = trailer[172,   5]  #Quantidade  de Registros- Ocorrência 19
    trail["valor_regs19"]            = trailer[177,  12] #Valor dos  Registros- Ocorrência 19
    trail["valor_total_rateios"]     = trailer[363,  15]
    trail["qtd_rateios"]             = trailer[378,   8]
    
    trail["sequencial"]              = trailer[395,   6]  #9  Seqüencial do registro



def cnab400():
    file = open("/home/jayme/Desktop/doois/gestorpsi/retorno-cb030400-bradesco.ret", 'r+')

    header = ""
    trailer = ""
    lines = []

    while True:
        line = file.readline()
        #print line
        if line == "":
            break
        #print "|"+line[0]+"|"
        if line[0] == '0': #header
            header = readHeader(" "+line)
        elif line[0] == '1': #detail
            lines.append( readDetail(" "+line) )
            break
        # em construcao
        elif line[0] == '9': #trailer
            trailer = readTrailer(" "+line)
        #print line
    file.close()

if __name__ == "__main__":
    cnab400()



'''

    /**Processa a linha trailer do arquivo.**/
                                                                                                            //X = ALFANUMÉRICO 9 = NUMÉRICO V = VÍRGULA DECIMAL ASSUMIDA
        $vlinha["registro"]                = substr($linha,   1,   1);  //9  Identificação do Registro Trailer: “9”
        $vlinha["retorno"]                 = substr($linha,   2,   1);  //9  “2”
        $vlinha["tipo_registro"]           = substr($linha,   3,   2);  //9  “01”
        $vlinha["cod_banco"]               = substr($linha,   5,   3);
        $vlinha["cob_simples_qtd_titulos"] = substr($linha,  18,   8);  //9  Cobrança Simples - quantidade de títulos em cobranca
        $vlinha["cob_simples_vlr_total"]   = $this->formataNumero(substr($linha,  26,  14)); //9  v99 Cobrança Simples - valor total
        $vlinha["cob_simples_num_aviso"]   = substr($linha,  40,   8);  //9  Cobrança Simples - Número do aviso
        $vlinha["qtd_regs02"]              = substr($linha,  58,   5);  //Quantidade  de Registros- Ocorrência 02 – Confirmação de Entradas
        $vlinha["valor_regs02"]            = $this->formataNumero(substr($linha,  63,  12)); //Valor dos Registros- Ocorrência 02 – Confirmação de Entradas
        $vlinha["valor_regs06liq"]         = $this->formataNumero(substr($linha,  75,  12)); //Valor dos Registros- Ocorrência 06 liquidacao
        $vlinha["qtd_regs06"]              = substr($linha,  87,   5);  //Quantidade  de Registros- Ocorrência 06 – liquidacao
        $vlinha["valor_regs06"]            = $this->formataNumero(substr($linha,  92,  12)); //Valor dos Registros- Ocorrência 06
        $vlinha["qtd_regs09"]              = substr($linha,  104,   5);  //Quantidade  de Registros- Ocorrência 09 e 10
        $vlinha["valor_regs02"]            = $this->formataNumero(substr($linha,  109,  12)); //Valor dos  Registros- Ocorrência 09 e 10
        $vlinha["qtd_regs13"]              = substr($linha,  121,   5);  //Quantidade  de Registros- Ocorrência 13
        $vlinha["valor_regs13"]            = $this->formataNumero(substr($linha,  126,  12)); //Valor dos  Registros- Ocorrência 13
        $vlinha["qtd_regs14"]              = substr($linha,  138,   5);  //Quantidade  de Registros- Ocorrência 14
        $vlinha["valor_regs14"]            = $this->formataNumero(substr($linha,  143,  12)); //Valor dos  Registros- Ocorrência 14
        $vlinha["qtd_regs12"]              = substr($linha,  155,   5);  //Quantidade  de Registros- Ocorrência 12
        $vlinha["valor_regs12"]            = $this->formataNumero(substr($linha,  160,  12)); //Valor dos  Registros- Ocorrência 12
        $vlinha["qtd_regs19"]              = substr($linha,  172,   5);  //Quantidade  de Registros- Ocorrência 19
        $vlinha["valor_regs19"]            = $this->formataNumero(substr($linha,  177,  12)); //Valor dos  Registros- Ocorrência 19
    $vlinha["valor_total_rateios"]     = $this->formataNumero(substr($linha,  363,  15));
    $vlinha["qtd_rateios"]             = substr($linha,  378,   8);

        $vlinha["sequencial"]              = substr($linha, 395,   6);  //9  Seqüencial do registro

'''
