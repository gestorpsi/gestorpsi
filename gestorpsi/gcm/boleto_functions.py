# -*- coding: utf-8 -*-

import datetime
import httplib
import urllib
import urllib2
import re


URL_GERADOR_BOLETOS = 'http://dev.geradorboletos.doois.com.br/bradesco/'
URL_GERADOR_BOLETOS = 'http://localhost:8080/boleto/bradesco/'
CHAVE_UNICA = ''



def gera_boleto_bradesco_teste():
    '''
    Receives a dict filled with the data that will be sent to the billet generator
    and returns a permalink to the billet generated.
    '''

    dados_teste = {}
    #INFORMANDO DADOS SOBRE O CEDENTE.
    dados_teste['cedente_nome'] = "Gestorpsi"
    dados_teste['cedente_cnpj'] = "00.000.208/0001-00"
    
    #INFORMANDO DADOS SOBRE O SACADO.
    dados_teste['sacado_nome'] = "JavaDeveloper Pronto Para Ferias"
    dados_teste['sacado_cpf'] = "222.222.222-22"
    
    #Informando o endereço do sacado.
    dados_teste['enderecosac_uf'] = "RN"
    dados_teste['enderecosac_localidade'] = "Natal"
    dados_teste['enderecosac_cep'] = "59064-120"
    dados_teste['enderecosac_bairro'] = "Grande Centro"
    dados_teste['enderecosac_logradouro'] = "Rua poeta dos programas"
    dados_teste['enderecosac_numero'] = "1"
    
    #INFORMANDO DADOS SOBRE O SACADOR AVALISTA.
    dados_teste['sacadoravalista_nome'] = "JRimum Enterprise"
    dados_teste['sacadoravalista_cnpj'] = "00.000.000/0001-91"
    
    #Informando o endereco do sacador avalista.
    dados_teste['enderecosacaval_uf'] = "DF"
    dados_teste['enderecosacaval_localidade'] = "Brasília"
    dados_teste['enderecosacaval_cep'] = "59000-000"
    dados_teste['enderecosacaval_bairro'] = "Grande Centro"
    dados_teste['enderecosacaval_logradouro'] = "Rua Eternamente Principal"
    dados_teste['enderecosacaval_numero'] = "001"
    
    #INFORMANDO OS DADOS SOBRE O TÍTULO.
    
    #Informando dados sobre a conta bancaria do titulo.
    #dados_teste['contabancaria'] = "BRADESCO"
    dados_teste['contabancaria_numerodaconta'] = "123456"
    dados_teste['contabancaria_numerodaconta_digito'] = "0"
    dados_teste['contabancaria_carteira'] = "30"
    dados_teste['contabancaria_agencia'] = "1234"
    dados_teste['contabancaria_agencia_digito'] = "1"
    
    dados_teste['titulo_numerododocumento'] = "123456"
    dados_teste['titulo_nossonumero'] = "99345678912"
    dados_teste['titulo_digitodonossonumero'] = "5"
    dados_teste['titulo_valor'] = "0.23"
    dados_teste['titulo_datadodocumento'] = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S") 
    dados_teste['titulo_datadovencimento'] = (datetime.datetime.now() + datetime.timedelta(days=10)).strftime("%y-%m-%d %H:%M:%S") 
    
    dados_teste['titulo_desconto'] = "0.05"
    dados_teste['titulo_deducao'] = "0"
    dados_teste['titulo_mora'] = "0"
    dados_teste['titulo_acrecimo'] = "0"
    dados_teste['titulo_valorcobrado'] = "0"
    
    #INFORMANDO OS DADOS SOBRE O BOLETO.
    dados_teste['boleto_localpagamento'] = "Pagável preferencialmente na Rede X ou em qualquer Banco até o Vencimento."
    dados_teste['boleto_instrucaoaosacado'] = "Senhor sacado, sabemos sim que o valor cobrado não é o esperado, aproveite o DESCONTÃO!"
    dados_teste['boleto_instrucao1'] = "PARA PAGAMENTO 1 até Hoje não cobrar nada!"
    dados_teste['boleto_instrucao2'] = "PARA PAGAMENTO 2 até Amanhã Não cobre!"
    dados_teste['boleto_instrucao3'] = "PARA PAGAMENTO 3 até Depois de amanhã, OK, não cobre."
    dados_teste['boleto_instrucao4'] = "PARA PAGAMENTO 4 até 04/xx/xxxx de 4 dias atrás COBRAR O VALOR DE: R$ 01,00"
    dados_teste['boleto_instrucao5'] = "PARA PAGAMENTO 5 até 05/xx/xxxx COBRAR O VALOR DE: R$ 02,00"
    dados_teste['boleto_instrucao6'] = "PARA PAGAMENTO 6 até 06/xx/xxxx COBRAR O VALOR DE: R$ 03,00"
    dados_teste['boleto_instrucao7'] = "PARA PAGAMENTO 7 até xx/xx/xxxx COBRAR O VALOR QUE VOCÊ QUISER!"
    dados_teste['boleto_instrucao8'] = "APÓS o Vencimento, Pagável Somente na Rede X."    
    
    for p in dados_teste:
        p = p.encode()
    
    url = URL_GERADOR_BOLETOS
    data = urllib.urlencode(dados_teste)
    #print datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S") 
    #raise Exception(url)
    req = urllib2.Request(url, data) #if the data parameter is here, it's a POST request
    response = urllib2.urlopen(req)
    the_page = response.read()

    if len(the_page) == 40:
        return url+the_page
    else:
        return the_page



def gera_boleto_bradesco(dados):
    '''
    Receives a dict filled with the data that will be sent to the billet generator
    and returns a permalink to the billet generated.
    '''
  
    url = URL_GERADOR_BOLETOS
    data = urllib.urlencode(dados)
    #print datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S") 
    #raise Exception(url)
    req = urllib2.Request(url, data) #if the data parameter is here, it's a POST request
    response = urllib2.urlopen(req)
    the_page = response.read()

    if len(the_page) == 40:
        return url+the_page
    else:
        return False

    
def main(argv=None):
    print gera_boleto_bradesco_teste()


if __name__ == "__main__":
    main()

