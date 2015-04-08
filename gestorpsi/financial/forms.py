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
from gestorpsi.financial.models import Payment, PaymentWay


class PaymentForm(forms.ModelForm):
    price = forms.DecimalField(max_digits=10, decimal_places=2, localize=True, widget=forms.TextInput( attrs={'class':'big','required':'required','placeholder':'1.234,56', 'id':"price", 'data-symbol':"R$ ", 'data-thousands':".", 'data-decimal':"," } ))

    off = forms.DecimalField(max_digits=10, decimal_places=2, localize=True, widget=forms.TextInput( attrs={'class':'big','required':'required','placeholder':'1.234,56', 'id':"off"} ))

    total = forms.DecimalField(max_digits=10, decimal_places=2, localize=True, widget=forms.TextInput( attrs={'class':'big','required':'required','placeholder':'1.234,56', 'id':"total"} ))

    #price = forms.DecimalField(
            #label='Valor',
            #decimal_places=2,
            #required=True,
            #)

    #payment_way = forms.Select( 
            ##label='Forma de pagamento',
            ##required=True,
            ##widget=forms.Select(attrs={'class':'big'}),
            ##queryset=PaymentWay.objects.all() 
            #)
    #covenant_payment_way_options = forms.ChoiceField( required=True, widget=forms.CheckboxInput( attrs={'class':'extrabig'} ))

    pass
        
    class Meta:
        model = Payment
        exclude = ['occurrence','covenant_pack_size','covenant_charge']
