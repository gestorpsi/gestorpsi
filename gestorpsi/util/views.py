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
    return "%.1f" % ((int(number)*100)/int(total))

