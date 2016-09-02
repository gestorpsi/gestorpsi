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

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from django.template.defaultfilters import slugify
from django.forms.util import ErrorList
from django.utils.translation import ugettext as _
from django.contrib.auth.views import login as django_login
from django.core.mail import EmailMessage

from gestorpsi.util.views import get_object_or_None
from gestorpsi.settings import SITE_DISABLED, ADMIN_URL, ADMINS_REGISTRATION, SIGNATURE, URL_DEMO, URL_APP, URL_HOME
from gestorpsi.organization.models import Organization, ProfessionalResponsible
from gestorpsi.gcm.models.invoice import Invoice
from gestorpsi.authentication.forms import RegistrationForm
from registration.models import RegistrationProfile

def login_check(f):
    '''
        login_check decorator
        code from http://code.activestate.com/recipes/498217/
        changed by czd@gestorpsi.com.br
    '''
    @login_required
    def wrap(request, *args, **kwargs):
        return f(request, *args, **kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap


def user_authentication(request):

    if SITE_DISABLED:
        return render_to_response('core/site_disabled.html')

    if not request.method == "POST":
        return render_to_response('authentication/authentication_login_form.html', {'form': AuthenticationForm() })

    form = AuthenticationForm(data=request.POST)
    username = request.POST.get('username').strip() # strip to remove all white space
    password = request.POST.get('password')
    
    # login Django, open session.
    user = authenticate(username=username, password=password)

    # user does not exist
    if not user:
        set_trylogin(username)
        messages.error(request, _('Invalid username or password'))
        return render_to_response('authentication/authentication_login_form.html', {'form': form }, context_instance=RequestContext(request))
    else:
        request.session['user_aux_id'] = user.id

    # redirect to admin page
    if user.is_staff or user.is_superuser:
        login(request, user)
        return HttpResponseRedirect(ADMIN_URL)

    # user has not confirmed registration yet
    if user.registrationprofile_set.all()[0].activation_key != 'ALREADY_ACTIVATED':
        form_messages = _('Your account has not been confirmated yet. Please check your email and use your activation code to continue')
        return render_to_response('authentication/authentication_login_form.html', {'form':form, 'form_messages': form_messages })
    
    if not user.is_active:
        form_messages = _('Your account has been disable. Please contact our support')
        return render_to_response('authentication/authentication_login_form.html', {'form':form, 'form_messages': form_messages })

    # none restriction to login from where.
    clear_login(user)
    # django login, user.profile is required
    login(request, user)

    # choose a organization
    if user.profile.organization.distinct().count() > 1:
        # redirect to select org page
        return HttpResponseRedirect(reverse('authentication-select-organization'))

    # just one organization
    else: 
        # load profile user
        user.profile.org_active = user.profile.organization.all()[0] # just one org
        user.profile.save()

        # new role
        user.groups.clear()
        for role in user.get_profile().role_set.filter(organization=user.profile.org_active):
            user.groups.add(role.group)

        # django login
        login(request, user)
        return HttpResponseRedirect('/')


def select_organization(request):
    """
        Select organization when user have more than one org.
        Change organization without logout of GPSI.
    """

    if not request.POST:
        return render_to_response('authentication/authentication_select_organization.html', { 'objects': request.user.profile.organization.distinct() })

    if request.POST:

        # selected org
        # check selected org, org cant be a user org list
        organization = get_object_or_None( Organization, pk=request.POST.get('organization') )

        if not organization in request.user.profile.organization.distinct():
            messages.error(request, _(u'Organização inválida e/ou não existe.'))
            return HttpResponseRedirect(reverse('authentication-select-organization'))


        # logoff and login of current org is not selected organization
        if not request.user.get_profile().org_active == organization:
            # load selected org
            request.user.get_profile().org_active = organization
            request.user.get_profile().save()

            # update roles according selected organization
            request.user.groups.clear()
            for role in request.user.get_profile().role_set.filter(organization=organization):
                request.user.groups.add(role.group)

            messages.success(request, _(u'Login para %s feito com sucesso.') % organization.name )

        return HttpResponseRedirect('/')


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
             template_name='registration/registration_organization_form.html',
             extra_context=None):

    if request.method == 'POST': #the full process of registration is done here

        form = form_class(data=request.POST)
        error_found = False

        # remember state and city if form error
        form.fields['city'].initial = request.POST.get('city')
        form.fields['state'].initial = request.POST.get('state')

        # check organization name
        if Organization.objects.filter(short_name__iexact = slugify(request.POST.get('shortname'))):
            error_msg = _(u"Informed organization is already registered. Please choose another name here or login with an existing account")
            form.errors["shortname"] = ErrorList([error_msg])
            error_found = True

        # check password
        if not request.POST.get('password1') == request.POST.get('password2'):
            error_msg = _(u"The confirmation of the new password is wrong")
            form.errors["password1"] = ErrorList([error_msg])
            form.errors["password2"] = ErrorList([error_msg])
            error_found = True

        # form is valid and no errors found
        if form.is_valid() and not error_found:

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
            i.status = 2 # free
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

            msg.body += u"IMPORTANTE: As informações inseridas no sistema podem ser editadas mas não apagadas. Por isso, se for necessário fazer testes com informações fictícias para entender como o sistema funciona, utilize a nossa versão de demonstração: http://demo.gestorpsi.com.br\n\n"

            msg.body += u"Endereço do GestorPSI: %s\n" % URL_APP
            msg.body += u"Usuário/Login  %s\n" % request.POST.get('username')
            msg.body += u"Senha  %s\n\n" % request.POST.get('password1')

            msg.body += u"%s" % SIGNATURE

            msg.to = [ user.email, ]
            msg.bcc =  bcc_list
            msg.send()
            
            return HttpResponseRedirect(reverse('registration-complete'))

    # mount form, new register
    else:
        form = form_class()
    
    # WHY THIS CODE ???
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
def complete(request):
    return render_to_response('registration/registration_organization_complete.html', context_instance=RequestContext(request) )
