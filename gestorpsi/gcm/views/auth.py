# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.forms.util import ErrorList
from gestorpsi.gcm.forms.auth import RegistrationForm
from gestorpsi.organization.models import Organization
from registration.models import RegistrationProfile
from django.core.mail import send_mail
from django.core.mail import EmailMessage, BadHeaderError

'''
from django-registration
'''

def register(request, success_url=None,
             form_class=RegistrationForm,
             template_name='registration/registration_form.html',
             extra_context=None):
    
    if request.method == 'POST': #the full process of registration is done here
        form = form_class(data=request.POST)

        if Organization.objects.filter(short_name__iexact = slugify(request.POST.get('shortname'))):
            form = form_class(data=request.POST) # organization already exists, escaping .. 
            error_msg = _(u"Informed organization is already registered. Please choose another name here or login with an existing account")
            form.errors["organization"] = ErrorList([error_msg])
        elif request.POST.get('username') != slugify(request.POST.get('username')):
            error_msg = _(u"Enter a valid username.")
            form.errors["username"] = ErrorList([error_msg])
        else:
            if form.is_valid():
                new_user = form.save(request)
    
                from gestorpsi.gcm.boleto_functions import gera_boleto_bradesco_teste
                url_boleto = gera_boleto_bradesco_teste()
                
                if not url_boleto:
                    url_boleto = ''
                
                bcc_list = ['jayme@doois.com.br', 'david@doois.com.br']
                msg = EmailMessage()
                msg.subject = 'Teste: Nova organizacao em gestorpsi.com.br'
                msg.body = 'Uma nova organizacao se registrou no GestorPSI. Para mais detalhes acessar https://gestorpsi.psico.net/gcm/'
                msg.body += '\n Boleto exemplo: '+url_boleto
                #msg.from = 'GestoPSI <webmaster@gestorpsi.com.br>'
                msg.to = ['webmaster@gestorpsi.com.br', ]
                msg.bcc =  bcc_list
                #msg.content_subtype = "text"  # Main content is now text/html
                msg.send()
                return HttpResponseRedirect(success_url or reverse('gcm-registration-complete'))
    else:
        form = form_class()
    
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return render_to_response(template_name,
                              { 'form': form },
                              context_instance=context)



def complete(request, success_url=None,
             template_name='gcm/registration_complete.html',
             extra_context=None):
    from gestorpsi.gcm.boleto_functions import *
    from django.contrib.auth.models import User
    from gestorpsi.document.models import Document, TypeDocument
    from gestorpsi.address.models import City, Address, Country
    request.session['user_aux_id'] = 12
    if 'user_aux_id' in request.session:
        user = User.objects.get( pk=int(request.session['user_aux_id']) )
        profile = user.get_profile()
        person = profile.person
        
        d = Document()
        t = TypeDocument.objects.get(description='CPF')
        cpf = person.document.get(typeDocument__id=t.id).document
        
        addr = endereco = person.address.all()[0]

        #if len(addr.addressLine2): text += " - %s" % addr.addressLine2
        #if len(addr.neighborhood): text += " - %s" % addr.neighborhood
        #if len(addr.zipCode): text += " - CEP: %s" % addr.zipCode
        #raise Exception( endereco.city.name )
        
        #person.organization.add(organization)
        #profile.org_active = organization                  #set org as active
        #profile.temp = self.cleaned_data['password1']      # temporary field (LDAP)
        #profile.person = person
        #profile.save()
        
        dados_teste = {}
        #INFORMANDO DADOS SOBRE O CEDENTE (quem vai receber).
        dados_teste['cedente_nome'] = "Sistema Gestorpsi"
        dados_teste['cedente_cnpj'] = "00.000.208/0001-00"
        
        #INFORMANDO DADOS SOBRE O SACADO (quem vai pagar).
        dados_teste['sacado_nome'] = person.name
        dados_teste['sacado_cpf'] = cpf
        
        #Informando o endereço do sacado.
        dados_teste['enderecosac_uf'] = str(endereco.city.state.shortName)
        dados_teste['enderecosac_localidade'] = endereco.city.name
        dados_teste['enderecosac_cep'] = endereco.zipCode
        dados_teste['enderecosac_bairro'] = str(endereco.neighborhood)
        dados_teste['enderecosac_logradouro'] = endereco.addressLine1
        dados_teste['enderecosac_numero'] = endereco.addressNumber
        
        #INFORMANDO DADOS SOBRE O SACADOR AVALISTA (aquele que é contactado em caso de problemas).
        dados_teste['sacadoravalista_nome'] = "Oliver Prado"
        dados_teste['sacadoravalista_cnpj'] = "00.000.000/0001-91"
        
        #Informando o endereço do sacador avalista.
        dados_teste['enderecosacaval_uf'] = "DF"
        dados_teste['enderecosacaval_localidade'] = "Brasília"
        dados_teste['enderecosacaval_cep'] = "59000-000"
        dados_teste['enderecosacaval_bairro'] = "Grande Centro"
        dados_teste['enderecosacaval_logradouro'] = "Rua Eternamente Principal"
        dados_teste['enderecosacaval_numero'] = "001"
        
        #INFORMANDO OS DADOS SOBRE O TÍTULO.
        
        #Informando dados sobre a conta bancaria do titulo.
        dados_teste['contabancaria_numerodaconta'] = "123456"
        dados_teste['contabancaria_numerodaconta_digito'] = "0"
        dados_teste['contabancaria_carteira'] = "30"
        dados_teste['contabancaria_agencia'] = "1234"
        dados_teste['contabancaria_agencia_digito'] = "1"
        
        #Código fornecido pelo Banco para identificação do título ou identificação 
        #do título atribuído pelo emissor do título de cobrança. 
        dados_teste['titulo_nossonumero'] = "99345678912"
        dados_teste['titulo_digitodonossonumero'] = "5"
        dados_teste['titulo_valor'] = "1.23"
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
        
        url_boleto = gera_boleto_bradesco(dados_teste)

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return render_to_response(template_name, locals(), context_instance=context)


def object_activate(request, *args, **kwargs):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/gcm/login/?next=%s' % request.path)

    o = Organization.objects.get(pk=kwargs['object_id'])
    for p in o.person_set.all():
        for rp in p.profile.user.registrationprofile_set.all():
            activation_key = rp.activation_key.lower() # Normalize before trying anything with it.
            RegistrationProfile.objects.activate_user(activation_key)
    request.user.message_set.create(message=_('Organizacao %s ativada com sucesso') % o.name)
    return HttpResponseRedirect('/gcm/orgpen/')
