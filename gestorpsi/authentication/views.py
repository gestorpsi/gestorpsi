# -*- coding: utf-8 -*-

"""
Copyright (C) 2008 GestorPsi

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.forms.util import ErrorList
from django.utils.translation import ugettext as _
from django.contrib.auth.views import login as django_login
from django.core.mail import EmailMessage


from gestorpsi.settings import SITE_DISABLED, ADMIN_URL, ADMINS_REGISTRATION, URL_APP, URL_HOME, SIGNATURE, URL_DEMO

from gestorpsi.organization.models import Organization, ProfessionalResponsible
from gestorpsi.gcm.models.invoice import Invoice

from gestorpsi.authentication.forms import RegistrationForm
from registration.models import RegistrationProfile



#
# login_check decorator
# code from http://code.activestate.com/recipes/498217/
# changed by czd@gestorpsi.com.br

def login_check(f):
    @login_required
    def wrap(request, *args, **kwargs):
        return f(request, *args, **kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap


def user_authentication(request):
    if SITE_DISABLED:
        return render_to_response('core/site_disabled.html')
    if request.method != "POST":
        return render_to_response('registration/login.html', {'form': AuthenticationForm() })
    form = AuthenticationForm(data=request.POST)
    username = request.POST.get('username').strip().lower()
    password = request.POST.get('password')
    
    if (unblocked_user(username)):
        user = authenticate(username=username, password=password)
        
        # user does not exist
        if user is None:
            set_trylogin(username)
            form_messages = _('Invalid username or password')
            return render_to_response('registration/login.html', {'form': form, 'form_messages': form_messages })
        else:
            request.session['user_aux_id'] = user.id
        if user.is_staff or user.is_superuser:
            login(request, user)
            return HttpResponseRedirect(ADMIN_URL)

        # user has not confirmed registration yet
        if user.registrationprofile_set.all()[0].activation_key != 'ALREADY_ACTIVATED':
            form_messages = _('Your account has not been confirmated yet. Please check your email and use your activation code to continue')
            return render_to_response('registration/login.html', {'form':form, 'form_messages': form_messages })
        
        if not user.is_active:
            form_messages = _('Your account has been disable. Please contact our support')
            return render_to_response('registration/login.html', {'form':form, 'form_messages': form_messages })
        else:
            clear_login(user)
            profile = user.get_profile()
            if profile.organization.distinct().count() > 1:
                try:
                    organization = profile.organization.get(short_name__iexact = request.POST.get('shortname'))
                    profile.org_active = organization
                    profile.save()
                    user.groups.clear()
                    for role in user.get_profile().role_set.filter(organization=organization):
                        user.groups.add(role.group)
                    login(request, user)
                    return HttpResponseRedirect('/')
                except Organization.DoesNotExist:
                    request.session['temp_user'] = user
                    return render_to_response('registration/select_organization.html', { 'objects': profile.organization.distinct() })
            login(request, user)
            return HttpResponseRedirect(request.POST.get('next') or '/')




def user_organization(request):
    organization = Organization.objects.get(pk=request.POST.get('organization'))
    user = request.session['temp_user']
    del request.session['temp_user']        
    user.get_profile().org_active = organization
    user.get_profile().save()

    """ Update roles according to selected organization """
    user.groups.clear()
    for role in user.get_profile().role_set.filter(organization=organization):
        user.groups.add(role.group)

    login(request, user)           
    return HttpResponseRedirect('/')



"""
def old_user_authentication(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        username = request.POST.get('username').strip().lower()
        password = request.POST.get('password')
        if(unblocked_user(username)):
            user = authenticate(username=username, password=password)   
            if user is not None:
                if user.is_active:
                    profile = user.get_profile()
                    request.session['temp_user'] = user                
                    clear_login(user)
                    if len(profile.organization.all()) > 1:                                                           
                        return render_to_response('registration/select_organization.html', { 'objects': profile.organization.all()}) 
                    else:
                        number_org = []
                        number_org = profile.organization.all()
                        profile.org_active = number_org[0]
                        login(request, user)                                        
                        return HttpResponseRedirect('/')
            else:
                    set_trylogin(username)
                    return render_to_response('registration/login.html', {'form':form })
    else:
        form = AuthenticationForm()
        return render_to_response('registration/login.html', { 'form':form } )

def old_user_organization(request):
    organization = Organization.objects.get(pk=request.POST.get('organization'))
    user = request.session['temp_user']
    del request.session['temp_user']        
    user.get_profile().org_active = organization
    user.get_profile().save()
    login(request, user)           
    return HttpResponseRedirect('/') 
"""


def set_trylogin(user):     
    filtered_user = User.objects.filter(username=user)
    if(len(filtered_user)):        
        found_user = filtered_user[0]    
        old_number = found_user.get_profile().try_login
        old_number += 1
        found_user.get_profile().try_login = old_number
        found_user.save()



def clear_login(user):
    user.get_profile().try_login = 0
    user.save()
    


def change_password(user,current_password, new_password):    
    if check_password(current_password):   
        user.set_password(new_password)
        org = user.get_profile().org_active
        user.get_profile().org_active = None
        user.save()
        user.get_profile().org_active = org       


    
def unblocked_user(username):
    user = get_object_or_404(User, username=username)
    
    if user.is_staff or user.is_superuser:
        return True
    
    profile = user.get_profile()
    value = profile.try_login
    if (value >= settings.PASSWORD_RETIRES):            
        return False
    
    return True



def gestorpsi_login(request, *args, **kwargs):
    if SITE_DISABLED:
        return render_to_response('core/site_disabled.html')
    return django_login(request, *args, **kwargs)



'''
    from django-registration
    organization form registration, new org.
'''

def register(request, success_url=None,
             form_class=RegistrationForm,
             template_name='registration/registration_form.html',
             extra_context=None):
    
    if request.method == 'POST': #the full process of registration is done here

        form = form_class(data=request.POST)

        # remember state and city if form error
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
                
                bcc_list = ADMINS_REGISTRATION

                msg = EmailMessage()
                msg.subject = u'Nova assinatura em %s' % URL_HOME
                msg.body = u'Uma nova organizacao se registrou no GestorPSI. Para mais detalhes acessar %s/gcm/\n\n' % URL_APP
                msg.body += u'Organização %s' % org
                msg.to = bcc_list
                msg.send()
                
                request.session['user_aux_id'] = user.id

                # message for client
                user = User.objects.get(id=request.session['user_aux_id'])
                msg = EmailMessage()
                msg.subject = u"Assinatura GestorPSI.com.br"

                msg.body = u"Olá, bom dia!\n\n"
                msg.body += u"Obrigado por assinar o GestorPsi.\nSua solicitação foi recebida pela nossa equipe. Sua conta está pronta para usar! "
                msg.body += u"Qualquer dúvida que venha ter é possível consultar os links abaixo ou então entrar em contato conosco através do formulário de contato.\n\n"

                msg.body += u"link funcionalidades: %s/funcionalidades/\n" % URL_HOME
                msg.body += u"link como usar: %s/como-usar/\n" % URL_HOME
                msg.body += u"link manual: %s/media/manual.pdf\n" % URL_DEMO
                msg.body += u"link contato: %s/contato/\n\n" % URL_HOME
                msg.body += u"Instruções no YouTube: https://www.youtube.com/channel/UC03EiqIuX72q-fi0MfWK8WA\n\n"

                msg.body += u"O periodo de teste inicia em %s e termina em %s.\n" % ( i.start_date.strftime("%d/%m/%Y"), i.end_date.strftime("%d/%m/%Y") )
                msg.body += u"Antes do término do período de teste você deve optar por uma forma de pagamento aqui: %s/organization/signature/\n\n" % URL_APP

                msg.body += u"Endereço do GestorPSI: %s\n" % URL_APP
                msg.body += u"Usuário/Login  %s\n" % request.POST.get('username')
                msg.body += u"Senha  %s\n\n" % request.POST.get('password1')

                msg.body += u"%s" % SIGNATURE

                msg.to = [ user.email, ]
                msg.bcc =  bcc_list
                msg.send()
                
                return HttpResponseRedirect(success_url or reverse('registration-complete'))
    else:
        form = form_class()
    
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return render_to_response(
                template_name,
                { 'form': form },
                context_instance=RequestContext(request)
            )




'''
    registration complete. New org
'''
def complete(request, success_url=None, extra_context=None):

    from gestorpsi.settings import URL_APP, URL_HOME

    return render_to_response('registration/registration_complete.html',
                locals(),
                context_instance=RequestContext(request)
            )

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

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    '''


"""
    confirm register after fill form, receive e-mail.
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
"""
