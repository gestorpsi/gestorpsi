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
            error_msg = _(u"Informed organization is already registered. Please choice another name here or login with an existing account")
            form.errors["organization"] = ErrorList([error_msg])
        elif request.POST.get('username') != slugify(request.POST.get('username')):
            error_msg = _(u"Enter a valid username.")
            form.errors["username"] = ErrorList([error_msg])
        else:
            if form.is_valid():
                new_user = form.save(request)
    
                from gcm.boleto_functions import gera_boleto_bradesco_teste
                url_boleto = gera_boleto_bradesco_teste()
                
                if not url_boleto:
                    url_boleto = ''
                
                bcc_list = ['jayme@doois.com.br', ]
                msg = EmailMessage()
                msg.subject = 'Nova organizacao em gestorpsi.com.br'
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
