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

from gestorpsi.financial.models import Payment
from gestorpsi.financial.forms import PaymentForm

def payment_form(request, obj=False):

    obj = get_object_or_404(Payment, pk=obj)

    if request.POST:
        print '--------------- 0'
    else:
        form = PaymentForm(instance=obj)

    return render_to_response( 'financial/financial_payment_form.html', locals(), context_instance=RequestContext(request) )
