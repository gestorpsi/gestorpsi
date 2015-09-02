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
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.template import RequestContext
from django.contrib import messages

from gestorpsi.financial.models import Receive
from gestorpsi.financial.forms import ReceiveFormUpdate

def receive_form(request, obj=False):

    obj = get_object_or_404(Receive, pk=obj)
    pfx = 'receive_form---%s' % obj.id # hardcore Jquery, mask currency

    if request.POST:

        form = ReceiveFormUpdate(request.POST , instance=obj, prefix=pfx)

        if form.is_valid():
            obj = form.save()
            messages.success(request, _(u'Salvo com sucesso!'))
            return HttpResponseRedirect('/financial/receive/%s/' % obj.id )

    # mount form
    else:
        form = ReceiveFormUpdate(instance=obj, prefix=pfx)


    # mount form or not valid form
    return render_to_response( 'financial/financial_receive_form.html', { 
            'form':form,
            'obj':obj
        }, context_instance=RequestContext(request) )
