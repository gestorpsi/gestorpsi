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
    
    #phone_save(object, request.POST.getlist('phoneId'), request.POST.getlist('area'), request.POST.getlist('phoneNumber'), request.POST.getlist('ext'), request.POST.getlist('phoneType'))
    
    def save_list(self, *args, **kwargs):
        raise Exception( self )
        def phone_list(ids, areas, numbers, exts, types): 
            objs = []
            for i in range(0, len(numbers)):
                if (len(numbers[i])):
                    objs.append(Phone(id=ids[i], area=areas[i], phoneNumber=numbers[i], ext=exts[i], phoneType=PhoneType.objects.get(pk=types[i])))
            return objs
        
        def phone_save(object, ids, areas, numbers, exts, types):
            object.phones.all().delete()
            for phone in phone_list(ids, areas, numbers, exts, types):
                phone.content_object = object
                phone.save()

