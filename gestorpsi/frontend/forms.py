# -*- coding: utf-8 -*-

"""
Copyright (C) 2012 GestorPsi

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
from gestorpsi.frontend.models import FrontendProfile


class FrontendProfileForm(forms.ModelForm):
    class Meta:
        fields = ('my_service','service','service_sort', 'schedule', 'referral', 'referral_sort', 'client', 'client_sort', 'queue','queue_sort', 'birthdate_client', 'subscribe_client', 'student')
        model = FrontendProfile