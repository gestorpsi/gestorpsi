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

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.mail import EmailMessage, BadHeaderError
from django.utils.translation import gettext as _
from django.template.context import RequestContext
from gestorpsi.support.forms import TicketForm
from gestorpsi.settings import EMAIL_FROM, ADMINS_REGISTRATION

def ticket_form(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            new = form.save(commit=False)
            new.user = request.user.profile.person
            new.save()
            body = ('%s\n\n%s\n%s\n%s') % (request.POST['question'], request.POST['contact_name'], request.POST['contact_phone'], request.POST['contact_email'] )
            email = EmailMessage(_('[GestorPsi] Support Request'), body, EMAIL_FROM , ADMINS_REGISTRATION, headers = {'Reply-To': request.POST['contact_email']} )

            try:
                email.send()
                return HttpResponseRedirect('/support/ticket/sent/')
            except BadHeaderError:
                return HttpResponse('Error on sending mail')
    else:
        initial = {
            'contact_name' : request.user.profile.person.name,
            'contact_phone' : request.user.profile.person.get_first_phone(),
            'contact_email' : request.user.profile.person.get_first_email(),
            }
        form = TicketForm(initial)
    return render_to_response('support/ticket_form.html', locals(), context_instance=RequestContext(request))
