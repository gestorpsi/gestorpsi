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
from gestorpsi.covenant.models import Covenant, CATEGORY, CHARGE, DEADLINE, PAYMENT_WAY


class CovenantForm(forms.ModelForm):

    category = forms.MultipleChoiceField( required=True, widget=forms.Select( attrs={'class':'extrabig'} ), choices=CATEGORY)
    charge = forms.MultipleChoiceField( required=True, widget=forms.Select( attrs={'class':'extrabig'} ), choices=CHARGE)
    deadline = forms.MultipleChoiceField( required=True, widget=forms.Select( attrs={'class':'extrabig'} ), choices=DEADLINE)
    price = forms.CharField( required=True, widget=forms.TextInput( attrs={'class':'big','required':'required','placeholder':'123,45', 'id':"numbersOnly"} ))
    payment_way = forms.MultipleChoiceField( required=True, widget=forms.CheckboxSelectMultiple(), choices=PAYMENT_WAY )

    class Meta:
        model = Covenant
