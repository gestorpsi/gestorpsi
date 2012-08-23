#from django.template import RequestContext
#from django.shortcuts import render_to_response
#from django.template.defaultfilters import slugify
#from gcm.forms.auth import RegistrationForm
#from gestorpsi.organization.models import Organization

#'''
#from django-registration
#'''
#def register(request, success_url=None,
             #form_class=RegistrationForm,
             #template_name='registration/registration_form.html',
             #extra_context=None):
    #if request.method == 'POST':
        #form = form_class(data=request.POST)

        #if Organization.objects.filter(short_name__iexact = slugify(request.POST.get('shortname'))):
            #form = form_class(data=request.POST) # organization already exists, escaping .. 
            #error_msg = _(u"Informed organization is already registered. Please choice another name here or login with an existing account")
            #form.errors["organization"] = ErrorList([error_msg])
        #elif request.POST.get('username') != slugify(request.POST.get('username')):
            #error_msg = _(u"Enter a valid username.")
            #form.errors["username"] = ErrorList([error_msg])
        #else:
            #if form.is_valid():
                #new_user = form.save()
                #return HttpResponseRedirect(success_url or reverse('registration_complete'))
    #else:
        #form = form_class()
    
    #if extra_context is None:
        #extra_context = {}
    #context = RequestContext(request)
    #for key, value in extra_context.items():
        #context[key] = callable(value) and value() or value
    #return render_to_response(template_name,
                              #{ 'form': form },
                              #context_instance=context)
