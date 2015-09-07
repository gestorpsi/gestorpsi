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

from ast import literal_eval
from django import forms
from gestorpsi.financial.models import Receive, PaymentWay



def get_choices(obj):
    '''
        obj : Receive.id
    '''
    obj = Receive.objects.get( pk=obj )

    try:
        return literal_eval(obj.covenant_payment_way_options)
    except:
        return PaymentWay.objects.none()


'''
    update a receive
    payment way exist
'''
class ReceiveFormUpdate(forms.ModelForm):
    name = forms.CharField(label=u'Nome convênio', max_length=250, widget=forms.TextInput( attrs={ 'readonly':'true' , 'class':'big' }) );
    price = forms.DecimalField(label=u"Valor", max_digits=10, decimal_places=2, localize=True, widget=forms.TextInput( attrs={'class':'big','required':'required','readonly':'true'} ) )
    off = forms.DecimalField(label=u"Desconto", max_digits=10, decimal_places=2, localize=True, widget=forms.TextInput( attrs={'class':'big','required':'required','placeholder':'1.234,56'} ))
    total = forms.DecimalField(label=u"Total", max_digits=10, decimal_places=2, localize=True, widget=forms.TextInput( attrs={'class':'big','required':'required','readonly':'true'} ) )

    class Meta:
        model = Receive
        exclude = ['occurrence','covenant_pack_size','covenant_charge','covenant_payment_way_options','covenant_id']


    def __init__(self, *args, **kwargs):

        super(ReceiveFormUpdate, self).__init__(*args, **kwargs)

        self.fields['covenant_payment_way_selected'] = forms.MultipleChoiceField(
            label=u'Forma de recebimento',
            required=False,
            widget=forms.CheckboxSelectMultiple( attrs={ 'class':'small' }),
            choices = get_choices( kwargs['instance'] )
        )


'''
    for group, create a receive
    payment way non exist becouse I don't know what covenant will be used
'''
class ReceiveFormNew(forms.ModelForm):
    name = forms.CharField(label=u'Nome convênio', max_length=250, widget=forms.TextInput( attrs={ 'readonly':'true' , 'class':'big' }) );
    price = forms.DecimalField(label=u"Valor", max_digits=10, decimal_places=2, localize=True, widget=forms.TextInput( attrs={'class':'big','readonly':'true'} ) )
    off = forms.DecimalField(label=u"Desconto", max_digits=10, decimal_places=2, localize=True, widget=forms.TextInput( attrs={'class':'big','placeholder':'1.234,56'} ))
    total = forms.DecimalField(label=u"Total", max_digits=10, decimal_places=2, localize=True, widget=forms.TextInput( attrs={'class':'big','readonly':'true'} ) )

    class Meta:
        model = Receive
        exclude = ['occurrence','covenant_pack_size','covenant_charge','covenant_payment_way_options','covenant_payment_way_selected','covenant_id']
