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

class Occupation(models.Model):
    """
    This class represents an occupation according to http://www.mte.gov.br
    @author: GestorPsi
    @version: 1.0
    """
    id = models.IntegerField(primary_key=True)
    cbo_code = models.CharField(max_length=999)
    title = models.CharField(max_length=999)

    def __unicode__(self):
        return u"%s" % self.title

class Synonyms(models.Model):
    """
    This class represents a synonyms that refers to an occupation
    @author: GestorPsi
    @version: 1.0
    """
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=999)
    occupation = models.ForeignKey(Occupation)

    def __unicode__(self):
        return u"%s" % self.title

