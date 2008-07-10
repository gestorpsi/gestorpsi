from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.utils.translation import gettext as _




def index(request):
    return render_to_response('core/main.html')
