from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.utils.translation import gettext as _
from gestorpsi.authentication.models import CustomUser

def index(request):
    
    if(request.user.is_authenticated()):
        return render_to_response('core/main.html')
    else:
        return render_to_response('registration/login.html')
