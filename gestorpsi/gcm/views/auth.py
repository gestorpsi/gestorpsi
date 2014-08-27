# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.forms.util import ErrorList
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib import messages

from gestorpsi.settings import ADMINS
from gestorpsi.gcm.forms.auth import RegistrationForm
from gestorpsi.gcm.models.invoice import Invoice
from gestorpsi.organization.models import Organization, ProfessionalResponsible                
from registration.models import RegistrationProfile

'''
    from django-registration
'''

def register(request, success_url=None,
             form_class=RegistrationForm,
             template_name='registration/registration_form.html',
             extra_context=None):
    
    if request.method == 'POST': #the full process of registration is done here

        form = form_class(data=request.POST)

        # remeber state and city if form error
        form.fields['city'].initial = request.POST.get('city')
        form.fields['state'].initial = request.POST.get('state')

        if Organization.objects.filter(short_name__iexact = slugify(request.POST.get('shortname'))):
            error_msg = _(u"Informed organization is already registered. Please choose another name here or login with an existing account")
            form.errors["organization"] = ErrorList([error_msg])

        elif request.POST.get('username') != slugify(request.POST.get('username')):
            error_msg = _(u"Enter a valid username.")
            form.errors["username"] = ErrorList([error_msg])

        else:
            if form.is_valid():
                form.save(request)

                user = User.objects.get(username__iexact=form.cleaned_data['username'])
                profile = user.get_profile()
                person = profile.person

                # active automatic
                org = Organization.objects.filter(organization__isnull=True).filter(person=person)[0]
                org.active = True
                org.save()
                for p in org.person_set.all():
                    for rp in p.profile.user.registrationprofile_set.all():
                        activation_key = rp.activation_key.lower() # Normalize before trying anything with it.
                        RegistrationProfile.objects.activate_user(activation_key)

                prof = ProfessionalResponsible()
                prof.organization = org
                prof.person = person
                prof.name = person.name
                prof.save()

                # invoice
                i = Invoice()
                i.organization = org
                i.status = 2
                i.save()
                
                bcc_list = ADMINS

                msg = EmailMessage()
                msg.subject = u'Nova assinatura em gestorpsi.com.br'
                msg.body = u'Uma nova organizacao se registrou no GestorPSI. Para mais detalhes acessar https://app.gestorpsi.com.br/gcm/\n\n'
                msg.body += u'Organização %s' % org
                msg.to = bcc_list
                msg.send()
                
                request.session['user_aux_id'] = user.id

                # message for client
                user = User.objects.get(id=request.session['user_aux_id'])
                msg = EmailMessage()
                msg.subject = u"Assinatura GestorPSI.com.br"

                msg.body = u"Olá, bom dia!\n\n"
                msg.body += u"Obrigado por assinar o GestorPsi.\nSua solicitação foi recebida pela nossa equipe e em breve você receberá outro email após a ativação da sua conta."
                msg.body += u"Qualquer dúvida que venha ter é possível consultar os links abaixo ou então entrar em contato conosco através do formulário de contato.\n\n"

                msg.body += u"link funcionalidades: http://portal.gestorpsi.com.br/funcionalidades/\n"
                msg.body += u"link como usar: http://portal.gestorpsi.com.br/como-usar/\n"
                msg.body += u"link manual: http://demo.gestorpsi.com.br/media/manual.pdf\n"
                msg.body += u"link contato: http://portal.gestorpsi.com.br/contato/\n\n"

                msg.body += u"Periodo de teste inicia em %s e termina em %s.\n\n" % ( i.date.strftime("%d/%m/%Y H%:i%"), i.due_date.strftime("%d/%m/%Y H%:%i") )
                msg.body += "Antes do término do período de teste você deve optar por uma forma de pagamento aqui:  https://app.gestorpsi.com.br/organization/signature/"
                msg.body += "<a href='https://app.gestorpsi.com.br/organization/signature/'>Assinatura</a>"

                msg.body += u"Endereço do sistema: http://app.gestorpsi.com.br\n"
                msg.body += u"Usuário/Login  %s\n" % request.POST.get('username')
                msg.body += u"Senha  %s\n\n" % request.POST.get('password1')

                msg.body += u"GestorPsi - Prontuários Eletrônicos e Gestão de Serviços em Psicologia.\n"
                msg.body += u"www.gestorpsi.com.br"

                msg.to = [ user.email, ]
                msg.bcc =  bcc_list
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



def complete(request, success_url=None, extra_context=None):

    template_name='gcm/registration_complete.html'

    '''
    from gestorpsi.boleto.functions import gera_boleto_bradesco_inscricao
    from django.contrib.auth.models import User
    from gestorpsi.document.models import Document, TypeDocument
    from gestorpsi.address.models import City, Address, Country

    if 'user_aux_id' in request.session:

        #url_boleto = gera_boleto_bradesco_inscricao(request.session['user_aux_id'])

        user = User.objects.get(id=request.session['user_aux_id'])
        
        bcc_list = ['teagom@gmail.com']
        msg = EmailMessage()
        msg.subject = u"Assinatura GestorPSI.com.br"

        msg.body = u"Olá, bom dia!\n\n.Primeiramente agradecemos a inscrição no sistema GestorPSI.com.br\n\n"
        msg.body += u"Em instantes você ira receber um boleto referênte ao plano que você escolheu.\n"
        msg.body += u"Qualquer dúvida que venha ter é possível consultar os links abaixo ou então entrar em contato conosco pelo link.\n"
        msg.body += u"link funcionalidades:   http://portal.gestorpsi.com.br/funcionalidades/\nlink como usar:  http://portal.gestorpsi.com.br/como-usar/\nlink manual:     http://demo.gestorpsi.com.br/media/manual.pdf\nlink contato:    http://portal.gestorpsi.com.br/contato/\n\n"
        msg.body += u"GestorPSI.com.br - Prontuários Eletrônicos e Gestão de Serviços em Psicologia"

        msg.body = u"Olá, bom dia!\n\n"
        msg.body += u"Obrigado por assinar o GestorPsi.\nSua solicitação foi recebida pela nossa equipe e em breve você receberá outro email após a ativação da sua conta."
        msg.body += u"Qualquer dúvida que venha ter é possível consultar os links abaixo ou então entrar em contato conosco através do formulário de contato.\n\n"

        msg.body += u"link funcionalidades: http://portal.gestorpsi.com.br/funcionalidades/\n"
        msg.body += u"link como usar: http://portal.gestorpsi.com.br/como-usar/\n"
        msg.body += u"link manual: http://demo.gestorpsi.com.br/media/manual.pdf\n"
        msg.body += u"link contato: http://portal.gestorpsi.com.br/contato/\n\n"

        msg.body += u"GestorPsi - Prontuários Eletrônicos e Gestão de Serviços em Psicologia.\n"
        msg.body += u"www.gestorpsi.com.br"

        msg.to = [ user.email, ]
        msg.bcc =  bcc_list
        msg.send()
    '''

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return render_to_response(template_name, locals(), context_instance=context)


"""
    confirm register
"""
def object_activate(request, *args, **kwargs):

    if not request.user.is_superuser:
        return HttpResponseRedirect('/gcm/login/?next=%s' % request.path)

    o = Organization.objects.get(pk=kwargs['object_id'])
    o.active = True
    o.save()
    for p in o.person_set.all():
        for rp in p.profile.user.registrationprofile_set.all():
            activation_key = rp.activation_key.lower() # Normalize before trying anything with it.
            RegistrationProfile.objects.activate_user(activation_key)
    
    messages.success(request, _('Organizacao %s ativada com sucesso') % o.name)
    return HttpResponseRedirect('/gcm/orgpen/')
