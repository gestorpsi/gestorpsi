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
# It's unused
# from django.utils.translation import ugettext_lazy as _
from gestorpsi.careprofessional.models import StudentProfile, Profession


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = (
            'lecture_class', 'period', 'class_duration', 'register_number')

    def __init__(self, *args, **kwargs):
        super(StudentProfileForm, self).__init__(*args, **kwargs)
        self.fields['lecture_class'].choices = [(
            i.id, i.academic_name) for i in Profession.objects.all()]
        self.fields['lecture_class'].widget.attrs = {'class': 'medium'}
        self.fields['register_number'].widget.attrs = {'class': 'big'}
