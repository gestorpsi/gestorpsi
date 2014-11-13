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

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.utils import simplejson

from gestorpsi.covenant.models import Covenant
from gestorpsi.covenant.forms import CovenantForm

"""
    Tiago de Souza Moraes
    tiago @ futuria com br
    13 11 2014
"""

def index(request):
    """
        covenant index, show all objects, list.
    """
    return render_to_response('covenant/covenant_index.html',
        {
            'obj_list': Covenant.objects.filter( organization=request.user.get_profile().org_active )
        },
        context_instance=RequestContext(request)
    )



def form(request, obj=False):
    """
        covenant form, update or save new
        obj: Covenant.id
    """

    if obj:
        obj = get_object_or_404(Covenant, pk=obj)

    if request.POST:

        # update
        if obj:
            form = CovenantForm(request.POST, instance=obj)
            obj = form.save()
            messages.success(request, _(u'Salvo com sucesso!'))
            return HttpResponseRedirect('/covenant/%s/edit/' % obj.id )

        # new
        else:
            form = CovenantForm(request.POST)

            if form.is_valid():
                obj = form.save(commit=False)
                obj.organization = request.user.get_profile().org_active
                obj.save()
                messages.success(request, _(u'Salvo com sucesso!'))
                return HttpResponseRedirect('/covenant/%s/edit/' % obj.id )

    # mount form
    else:
        if obj:
            form = CovenantForm(instance=obj)
        else:
            form = CovenantForm()

    return render_to_response('covenant/covenant_form.html',
                                {
                                    'form': form,
                                    'obj': obj,
                                },
                                context_instance=RequestContext(request)
    )




def list_json(request, deactive=True):
    """
        return object list in json format
    """

    if not deactive:
        obj_list = Covenant.objects.filter(active=False)
    else:
        obj_list = Covenant.objects.filter(active=True)

    covenant = {} # json
    c = 0

    for o in obj_list:
        covenant[c] = {
            'id': o.id,
            'name': u'%s' % o.name,
            'price': u'%s' % o.price,
        }
        c += 1

    return HttpResponse(simplejson.dumps(covenant, encoding = 'iso8859-1'), mimetype='application/json')
