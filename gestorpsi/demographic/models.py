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

import reversion
from django.db import models
from gestorpsi.cbo.models import Occupation
from gestorpsi.demographic.choices import *
from gestorpsi.client.models import Client

class Profession(models.Model):
    profession = models.ForeignKey(Occupation, null=True)
    synonyms =  models.CharField(max_length=999, null=True)
    labor_market_status = models.CharField(max_length=2, choices=LABOR_MARKET_STATUS)
    workplace = models.TextField(blank=True)
    working_hours = models.TextField(blank=True)
    status = models.BooleanField(default=True)
    comments = models.TextField(blank=True)
    client = models.ForeignKey(Client, null=True)

    def __unicode__(self):
        return u"%s" % self.profession
    
    class Meta:
        ordering = ['-status']

class EducationalLevel(models.Model):
    school_grade = models.CharField(max_length=2, choices=EDUCATION_LEVEL)
    comments = models.TextField(blank=True)
    client = models.OneToOneField(Client, null=True)
        
    def __unicode__(self):
        return u"%s" % self.get_school_grade_display()

reversion.register(Profession)
reversion.register(EducationalLevel)
