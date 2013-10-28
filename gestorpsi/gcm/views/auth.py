# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.forms.util import ErrorList
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.mail import EmailMessage, BadHeaderError
from django.contrib import messages

from gestorpsi.gcm.forms.auth import RegistrationForm
from gestorpsi.organization.models import Organization, ProfessionalResponsible                

from gestorpsi.authentication.models import Profile
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

        if Organization.objects.filter(short_name__iexact = slugify(request.POST.get('shortname'))):
            form = form_class(data=request.POST) # organization already exists, escaping .. 
            error_msg = _(u"Informed organization is already registered. Please choose another name here or login with an existing account")
            form.errors["organization"] = ErrorList([error_msg])
        elif request.POST.get('username') != slugify(request.POST.get('username')):
            error_msg = _(u"Enter a valid username.")
            form.errors["username"] = ErrorList([error_msg])
        else:
            if form.is_valid():
                form.save(request)

                #from gestorpsi.boleto.functions import *
                user = User.objects.get(username__iexact=form.cleaned_data['username'])
                profile = user.get_profile()
                person = profile.person
                org = Organization.objects.filter(organization__isnull=True).filter(person=person)[0]
                prof = ProfessionalResponsible()
                prof.organization = org
                prof.person = person
                prof.name = person.name
                prof.save()
                
                #url_boleto = gera_boleto_bradesco_inscricao( user.id )
                #if not url_boleto:
                #    url_boleto = ''
                
                bcc_list = ['kalkehcoisa@gmail.com']
                msg = EmailMessage()
                msg.subject = 'Teste: Nova organizacao em gestorpsi.com.br'
                msg.body = 'Uma nova organizacao se registrou no GestorPSI. Para mais detalhes acessar https://gestorpsi.psico.net/gcm/'
                #msg.body += '\n Boleto exemplo: '+url_boleto
                #msg.from = 'GestoPSI <webmaster@gestorpsi.com.br>'
                msg.to = ['webmaster@gestorpsi.com.br', ]
                msg.bcc =  bcc_list
                #msg.content_subtype = "text"  # Main content is now text/html
                msg.send()
                
                request.session['user_aux_id'] = user.id
                
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
             extra_context=None):
    template_name='gcm/registration_complete.html'
    from gestorpsi.boleto.functions import *
    from django.contrib.auth.models import User
    from gestorpsi.document.models import Document, TypeDocument
    from gestorpsi.address.models import City, Address, Country

    if 'user_aux_id' in request.session:
        url_boleto = gera_boleto_bradesco_inscricao(request.session['user_aux_id'])

        user = User.objects.get(id=request.session['user_aux_id'])
        
        bcc_list = ['kalkehcoisa@gmail.com']
        msg = EmailMessage()
        msg.subject = u"Teste: Nova organizacao em gestorpsi.com.br"
        msg.body = u"Você acaba de registrar uma nova organizacao se registrou no GestorPSI.<br/>"
        msg.body += u"Para que sua inscrição tenha seja confirmada e você possa começar a usar o sistema "
        msg.body += u"é preciso pagar o seguinte boleto: %s" % url_boleto
        #msg.from = 'GestoPSI <webmaster@gestorpsi.com.br>'
        msg.to = [user.email, ]
        msg.bcc =  bcc_list
        #msg.content_subtype = "text"  # Main content is now text/html
        msg.send()


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
    o.active = True
    o.save()
    for p in o.person_set.all():
        for rp in p.profile.user.registrationprofile_set.all():
            activation_key = rp.activation_key.lower() # Normalize before trying anything with it.
            RegistrationProfile.objects.activate_user(activation_key)
    
    messages.success(request, _('Organizacao %s ativada com sucesso') % o.name)
    return HttpResponseRedirect('/gcm/orgpen/')
