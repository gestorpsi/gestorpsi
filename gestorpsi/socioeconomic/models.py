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
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from gestorpsi.person.models import Person
from gestorpsi.util.uuid_field import UuidField
from gestorpsi.socioeconomic.choices import *
from gestorpsi.client.models import Client

class Transportation(models.Model):
    transportation = models.CharField(max_length=2, choices=TRANSPORTATION_TYPE)
    travel_time =  models.CharField(max_length=30, blank=True)
    client = models.ForeignKey(Client, null=True)
    comments = models.TextField(blank=True)

class Income(models.Model):
    individual_earning = models.CharField(max_length=2, choices=INCOME_RANGE)
    household_income = models.CharField(max_length=2, choices=INCOME_RANGE)
    client = models.OneToOneField(Client, null=True)
    comments = models.TextField(blank=True)

class IncomeSource(models.Model):
    income_source = models.CharField(max_length=2, choices=INCOME_SOURCE)
    income = models.ForeignKey(Income, null=True)
    comments = models.TextField(blank=True)
    
class Housing(models.Model):
    client = models.OneToOneField(Client, null=True)
    comments = models.TextField()

class Possession(models.Model):
    housing = models.ForeignKey(Housing, null=True)
    item = models.CharField(max_length=2, choices=POSSESSION_ITEMS)
    quantity = models.IntegerField()
    comments = models.TextField(blank=True)

class Eletricity(models.Model):
    housing = models.OneToOneField(Housing, null=True)
    eletricity = models.CharField(max_length=2, choices=ELETRICITY_TYPE)
    comments = models.TextField(blank=True)

class Sanitation(models.Model):
    housing = models.OneToOneField(Housing, null=True)
    water_supply = models.CharField(max_length=2, choices=WATER_SUPPLY_TYPE)
    water_treatment = models.CharField(max_length=2, choices=WATER_SUPPLY_TREATMENT_TYPE)
    sewer = models.CharField(max_length=2, choices=SEWER_TYPE)
    waste_disposition = models.CharField(max_length=2, choices=WASTE_DISPOSITION_TYPE)
    comments = models.TextField(blank=True)

class Paving(models.Model):
    housing = models.OneToOneField(Housing, null=True)
    paved_street = models.BooleanField()
    paviment_type = models.CharField(max_length=2, choices=PAVIMENT_TYPE)
    comments = models.TextField(blank=True)

class DwellingFeatures(models.Model):
    housing = models.OneToOneField(Housing, null=True)
    location = models.CharField(max_length=2, choices=LOCATION_TYPE)
    situation = models.CharField(max_length=2, choices=SITUATION_TYPE)
    dwelling_type = models.CharField(max_length=2, choices=DWELLING_TYPE)
    rooms = models.IntegerField()
    construction_type = models.CharField(max_length=2, choices=CONSTRUCTION_TYPE)
    covering_floor = models.CharField(max_length=2, choices=FLOOR_TYPE)
    roof_material = models.CharField(max_length=2, choices=ROOF_TYPE)
    coating_walls = models.BooleanField()
    comments = models.TextField(blank=True)

class PeopleHousehold(models.Model):
    housing = models.OneToOneField(Housing, null=True)
    number_of_people = models.IntegerField()
    head_family_edulevel = models.CharField(max_length=2, choices=EDUCATION_LEVEL)
    comments = models.TextField(blank=True)

