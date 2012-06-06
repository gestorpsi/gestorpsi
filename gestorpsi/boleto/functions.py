# -*- coding: utf-8 -*-

import datetime
import httplib
import urllib
import urllib2
import re

from django.utils.encoding import smart_str, force_unicode
from gestorpsi.boleto.models import BradescoBilletData
from django.contrib.auth.models import User
from gestorpsi.document.models import Document, TypeDocument
from gestorpsi.address.models import City, Address, Country

from gestorpsi.gcm.models import Plan, Invoice
from gestorpsi.organization.models import Organization


URL_GERADOR_BOLETOS = 'http://dev.geradorboletos.doois.com.br/bradesco/'
#URL_GERADOR_BOLETOS = 'http://localhost:8080/boleto/bradesco/'
CHAVE_UNICA = ''


def gera_boleto_bradesco(resp_usuario_id, invoice=None, days=7):
    '''
    Receives a dict filled with the data that will be sent to the billet generator
    and returns a permalink to the billet generated.
    '''
    
    user = User.objects.get( pk=int(resp_usuario_id) )
    profile = user.get_profile()
    person = profile.person

    d = Document()
    t = TypeDocument.objects.get(description='CPF')
    cpf = person.document.get(typeDocument__id=t.id).document
    addr = endereco = person.address.all()[0]
    data = BradescoBilletData.objects.all()[0]
    
    org = Organization.objects.filter(organization__isnull=True).filter(person__profile__user=user)[0]
    if invoice is None:
        inv = Invoice.objects.filter(organization=org, status=1).order_by('-expiry_date')[0]
        temp = (datetime.datetime.now() + datetime.timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
        inv.due_date = temp
        inv.save()
    else:
        inv = invoice


    if inv.billet_url is not None and len(inv.billet_url) > 5:
        return inv.billet_url
    else:
        dados = {}
        #INFORMANDO DADOS SOBRE O CEDENTE (quem vai receber).
        dados['cedente_nome'] = data.cedente_nome
        dados['cedente_cnpj'] = data.cedente_cnpj
        
        #INFORMANDO DADOS SOBRE O SACADO (quem vai pagar).
        dados['sacado_nome'] = person.name
        dados['sacado_cpf'] = cpf
        
        #Informando o endereço do sacado.
        try:
            dados['enderecosac_uf'] = str(endereco.city.state.shortName)
        except:
            dados['enderecosac_uf'] = ''
        try:
            dados['enderecosac_localidade'] = endereco.city.name
        except:
            dados['enderecosac_localidade'] = ''
        try:
            dados['enderecosac_cep'] = endereco.zipCode
        except:
            dados['enderecosac_cep'] = ''
        try:
            dados['enderecosac_bairro'] = str(endereco.neighborhood)
        except:
            dados['enderecosac_bairro'] = ''
        try:
            dados['enderecosac_logradouro'] = endereco.addressLine1
        except:
            dados['enderecosac_logradouro'] = ''
        try:
            dados['enderecosac_numero'] = endereco.addressNumber
        except:
            dados['enderecosac_numero'] = ''
        
        #INFORMANDO DADOS SOBRE O SACADOR AVALISTA (aquele que é contactado em caso de problemas).
        dados['sacadoravalista_nome'] = data.sacadoravalista_nome
        dados['sacadoravalista_cnpj'] = data.sacadoravalista_cnpj
        
        #Informando o endereço do sacador avalista.
        dados['enderecosacaval_uf'] = data.enderecosacaval_uf.shortName
        dados['enderecosacaval_localidade'] = data.enderecosacaval_localidade 
        dados['enderecosacaval_cep'] = data.enderecosacaval_cep
        dados['enderecosacaval_bairro'] = data.enderecosacaval_bairro
        dados['enderecosacaval_logradouro'] = data.enderecosacaval_logradouro
        dados['enderecosacaval_numero'] = data.enderecosacaval_numero
        
        #INFORMANDO OS DADOS SOBRE O TÍTULO.
        
        #Informando dados sobre a conta bancaria do titulo.
        dados['contabancaria_numerodaconta'] = data.contabancaria_numerodaconta
        dados['contabancaria_numerodaconta_digito'] = data.contabancaria_numerodaconta_digito
        dados['contabancaria_carteira'] = data.contabancaria_carteira
        dados['contabancaria_agencia'] = data.contabancaria_agencia
        dados['contabancaria_agencia_digito'] = data.contabancaria_agencia_digito
        
        #Código fornecido pelo Banco para identificação do título ou identificação 
        #do título atribuído pelo emissor do título de cobrança. 
        dados['titulo_nossonumero'] = data.titulo_nossonumero
        dados['titulo_digitodonossonumero'] = data.titulo_digitodonossonumero
        
        
    
        dados['titulo_deducao'] = "0.00"
        dados['titulo_mora'] = "0.00"
        dados['titulo_acrecimo'] = "0.00"
        dados['titulo_valorcobrado'] = "0.00"
        dados['titulo_desconto'] = "0.00"
        dados['titulo_valor'] = str(inv.ammount)
        dados['titulo_datadodocumento'] = str(inv.date)
        dados['titulo_datadovencimento'] = str(inv.due_date)
        
        #INFORMANDO OS DADOS SOBRE O BOLETO.
        dados['boleto_localpagamento'] = "Pagável preferencialmente no Bradesco."
        dados['boleto_instrucaoaosacado'] = "Pode ser pago em quaisquer agências."
        dados['boleto_instrucao1'] = "Após vencimento cobrar 50% de multa e 100% de juros ao dia."
        #dados['boleto_instrucao2'] = "PARA PAGAMENTO 2 até Amanhã Não cobre!"
        #dados['boleto_instrucao3'] = "PARA PAGAMENTO 3 até Depois de amanhã, OK, não cobre."
        #dados['boleto_instrucao4'] = "PARA PAGAMENTO 4 até 04/xx/xxxx de 4 dias atrás COBRAR O VALOR DE: R$ 01,00"
        #dados['boleto_instrucao5'] = "PARA PAGAMENTO 5 até 05/xx/xxxx COBRAR O VALOR DE: R$ 02,00"
        #dados['boleto_instrucao6'] = "PARA PAGAMENTO 6 até 06/xx/xxxx COBRAR O VALOR DE: R$ 03,00"
        #dados['boleto_instrucao7'] = "PARA PAGAMENTO 7 até xx/xx/xxxx COBRAR O VALOR QUE VOCÊ QUISER!"
        #dados['boleto_instrucao8'] = "APÓS o Vencimento, Pagável Somente na Rede X."   
        
        for p in dados.keys():
            dados[p] = smart_str(dados[p])
      
      
        url = URL_GERADOR_BOLETOS
        data = urllib.urlencode(dados)
        #print datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S") 
        #raise Exception(url)
        req = urllib2.Request(url, data) #if the data parameter is here, it's a POST request
        response = urllib2.urlopen(req)
        the_page = response.read()
    
        if len(the_page) == 40:
            inv.billet_url = url+the_page
            inv.save()
            return url+the_page
        else:
            return False




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
    dados_teste['titulo_acrecimo'] = "10.00"
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
        p = smart_str(p).decode('utf-8')
    
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


def main(argv=None):
    print gera_boleto_bradesco_teste()


if __name__ == "__main__":
    main()

