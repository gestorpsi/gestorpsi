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

from django import forms
from gestorpsi.support.models import Ticket

class TicketForm(forms.ModelForm):
    contact_email = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'extrabig', }))
    contact_phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'extrabig', }))
    contact_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'extrabig', }))
    question = forms.CharField(widget=forms.Textarea(attrs={'class':'extrabig', }), required=True)
    
    class Meta:
        fields = ('contact_email', 'contact_phone', 'contact_name', 'question')
        model = Ticket

