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
from django.db.models.query import QuerySet
from django.db.models.manager import Manager
from django.db.models.base import ModelBase

from gestorpsi.settings import SITE_DISABLED, ADMIN_URL, ADMINS_REGISTRATION, URL_APP, URL_HOME, SIGNATURE, URL_DEMO

from gestorpsi.organization.models import Organization, ProfessionalResponsible
from gestorpsi.gcm.models.invoice import Invoice
from gestorpsi.util.views import get_object_or_None
from gestorpsi.authentication.forms import RegistrationForm
from registration.models import RegistrationProfile

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
            return return_invalid_username(form)
        else:
            request.session['user_aux_id'] = user.id

        login_for_admin_or_staff(user, request)

        user_registration_not_confirmed(user, form)
        return login_active_user(user, form, request)

    else:
        return return_invalid_username(form)

def login_active_user(user, form, request):
    if not user.is_active:
        form_messages = _('Your account has been disable. Please contact our support')
        return render_to_response('registration/login.html', {'form':form, 'form_messages': form_messages })
    else:
        return login_user(user, request)

def user_registration_not_confirmed(user, form):
    if user.registrationprofile_set.all()[0].activation_key != 'ALREADY_ACTIVATED':
        form_messages = _('Your account has not been confirmated yet. Please check your email and use your activation code to continue')
        return render_to_response('registration/login.html', {'form':form, 'form_messages': form_messages })

def login_for_admin_or_staff(user, request):
    if user.is_staff or user.is_superuser:
        login(request, user)
        return HttpResponseRedirect(ADMIN_URL)

def login_user(user, request):
    clear_login(user)
    profile = user.get_profile()
    handle_multiple_organizations(profile, request, user)
    login(request, user)
    return HttpResponseRedirect(request.POST.get('next') or '/')

def handle_multiple_organizations(profile, request, user):
    if profile.organization.distinct().count() > 1:
        try:
            save_organization_shortname(profile, request)
            assign_role(user, request)
            return HttpResponseRedirect('/')
        except Organization.DoesNotExist:
            request.session['temp_user'] = user
            return render_to_response('registration/select_organization.html', { 'objects': profile.organization.distinct() })

def assign_role(user, request):
    user.groups.clear()
    for role in user.get_profile().role_set.filter(organization=organization):
        user.groups.add(role.group)
    login(request, user)

def return_invalid_username(form):
    form_messages = _('Invalid username or password')
    return render_to_response('registration/login.html', {'form': form, 'form_messages': form_messages })

def save_organization_shortname(profile, request):
    organization = profile.organization.get(short_name__iexact = request.POST.get('shortname'))
    profile.org_active = organization
    profile.save()
    
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
    user = get_object_or_None(User, username=username)
    if user == None:
        return False
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

                org = Organization.objects.filter(organization__isnull=True).filter(person=person)[0]

                activate_organization(org)

                activate_each_registered_profile (org)

                save_professional(org, person)

                organzation_invoice = Invoice()
                save_organization_invoice(organzation_invoice,org)
                
                bcc_list = ADMINS_REGISTRATION

                send_email_message_new_signature(bcc_list, org)
                
                request.session['user_aux_id'] = user.id

                message_for_client(organzation_invoice, request, bcc_list)

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

def activate_organization(org):
    org.active = True   
    org.save()

def message_for_client(organzation_invoice, request, bcc_list):
    user = User.objects.get(id=request.session['user_aux_id'])
    message = EmailMessage()
    message.subject = u"Assinatura GestorPSI.com.br"

    message.body = u"Olá, bom dia!\n\n"
    message.body += u"Obrigado por assinar o GestorPsi.\nSua solicitação foi recebida pela nossa equipe. Sua conta está pronta para usar! "
    message.body += u"Qualquer dúvida que venha ter é possível consultar os links abaixo ou então entrar em contato conosco através do formulário de contato.\n\n"

    message.body += u"link funcionalidades: %s/funcionalidades/\n" % URL_HOME
    message.body += u"link como usar: %s/como-usar/\n" % URL_HOME
    message.body += u"link manual: %s/media/manual.pdf\n" % URL_DEMO
    message.body += u"link contato: %s/contato/\n\n" % URL_HOME
    message.body += u"Instruções no YouTube: https://www.youtube.com/channel/UC03EiqIuX72q-fi0MfWK8WA\n\n"

    message.body += u"O periodo de teste inicia em %s e termina em %s.\n" % ( organzation_invoice.start_date.strftime("%d/%m/%Y"), organzation_invoice.end_date.strftime("%d/%m/%Y") )
    message.body += u"Antes do término do período de teste você deve optar por uma forma de pagamento aqui: %s/organization/signature/\n\n" % URL_APP

    message.body += u"Endereço do GestorPSI: %s\n" % URL_APP
    message.body += u"Usuário/Login  %s\n" % request.POST.get('username')
    message.body += u"Senha  %s\n\n" % request.POST.get('password1')

    message.body += u"%s" % SIGNATURE

    message.to = [ user.email, ]
    message.bcc =  bcc_list
    message.send()

def save_organization_invoice(organzation_invoice, org):
    organzation_invoice.organization = org
    organzation_invoice.status = 2
    organzation_invoice.save()

def send_email_message_new_signature (bcc_list, org):
    message = EmailMessage()
    message.subject = u'Nova assinatura em %s' % URL_HOME
    message.body = u'Uma nova organizacao se registrou no GestorPSI. Para mais detalhes acessar %s/gcm/\n\n' % URL_APP
    message.body += u'Organização %s' % org
    message.to = bcc_list
    message.send()

def save_professional(org, person):
    prof = ProfessionalResponsible()
    prof.organization = org
    prof.person = person
    prof.name = person.name
    prof.save()

def activate_each_registered_profile (org):
    for p in org.person_set.all():
        for rp in p.profile.user.registrationprofile_set.all():
            activation_key = rp.activation_key.lower() # Normalize before trying anything with it.
            RegistrationProfile.objects.activate_user(activation_key)

def complete(request, success_url=None, extra_context=None):

    return render_to_response('registration/registration_complete.html',
                locals(),
                context_instance=RequestContext(request)
            )

