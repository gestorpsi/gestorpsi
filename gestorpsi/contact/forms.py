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

from django.db import models
from django import forms

from gestorpsi.contact.models import Phone, PhoneType
from gestorpsi.contact.helpers import *


class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
    
    def __init__(self, *args, **kwargs):
        super(PhoneForm, self).__init__(*args, **kwargs)


class PhonesForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super(PhonesForm, self).__init__(*args, **kwargs)
    
    










