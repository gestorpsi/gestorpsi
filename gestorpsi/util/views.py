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

import ho.pisa as pisa
import cStringIO as StringIO
import cgi
import random
from django import http
from django.http import HttpResponse
from django.utils import simplejson
from django.template.loader import get_template
from django.template import Context
from gestorpsi.util.models import Cnae
from gestorpsi.cbo.models import Occupation


def get_object_or_new(klass, *args, **kwargs):
    # bitbucket.org/offline/django-annoying/src/tip/annoying/functions.py
    from django.shortcuts import _get_queryset
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return klass()


def get_object_or_None(klass, *args, **kwargs):
    """ Usage:
        from gestorpsi.util.views import get_object_or_None
        ...
        object = get_object_or_None(Class, pk=id)
    """
    from django.shortcuts import _get_queryset
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


def cnae(request):
    '''
    filter Cnae's return a dict with cnae codes and sub classes names 
    '''
    results = []
    for i in Cnae.objects.filter(cnae_class__icontains=request.GET.get('query')):
        results.append({'id': i.id, 'name': i.cnae_class})
    
    return HttpResponse(simplejson.dumps(results))


def ocupation(request):
    '''
    filter Cnae's return a dict with cnae codes and sub classes names 
    '''
    results = []
    for i in Occupation.objects.filter(title__icontains=request.GET.get('query')):
        results.append({'id': i.cbo_code, 'name': i.title })
    
    return HttpResponse(simplejson.dumps(results))


def write_pdf(template_src, context_dict, filename='output.pdf'):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(
        html.encode("UTF-8")), result)
    if not pdf.err:
        response =  HttpResponse(result.getvalue(), mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response
    return http.HttpResponse('Erro making pdf! %s' % cgi.escape(html))


def percentage(number, total):
    if not total:
        return 0
    return "%.1f" % ((int(number)*100.0)/int(total))


def color_rand():
    # generate a random color in hexaformat: DDEE44
    a = "%x" % random.randint(0, 16777215)
    a = '%s0' % a
    return a[:6]
    

def _access_check_referral_write(request, referral=None):
    """
    this method checks if professional as users when accessing clients
    @referral: referral object
    """
    # new referral form
    if not referral.id:
        return True

    # check if user is professional and not admin or secretary. if it's true, check if professional has referral with this customer
    if request.user.groups.filter(name='administrator') or request.user.groups.filter(name='secretary'):
        return True

    # check if professional or student
    if request.user.groups.filter(name='professional') or request.user.groups.filter(name='student'):

        professional_have_referral_with_client = False
        professional_is_responsible_for_service = False

        # lets check if request.user (professional) have referral with this client
        if request.user.profile.person.careprofessional in [p for p in referral.professional.all()]:
            professional_have_referral_with_client = True

        # lets check if request.user (professional) is responsible for this referral service
        if request.user.profile.person.careprofessional in [p for p in referral.service.responsibles.all()]:
            professional_is_responsible_for_service = True

        if professional_have_referral_with_client or professional_is_responsible_for_service:
            return True

    return False
