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
from gestorpsi.person.models import Person
from gestorpsi.admission.models import AdmissionReferral, Indication
from gestorpsi.util.uuid_field import UuidField
from gestorpsi.util import audittrail

class Relation(models.Model):
    description = models.CharField(max_length=30)
    def __unicode__(self):
        return u"%s" % self.description

class PersonLink(models.Model):
    person = models.OneToOneField(Person)
    relation = models.ForeignKey(Relation)
    responsible = models.BooleanField(default=False)
    def __unicode__(self):
        return u"%s" % self.person.name

class IdRecordSeq(models.Model):
    uid = models.CharField(max_length=100)

# CREATE SEQUENCE id_Record_Seq;
# ALTER TABLE client_client ALTER COLUMN idrecord TYPE integer DEFAULT nextval('id_record_seq') NOT NULL;
# ALTER TABLE client_client ALTER COLUMN idRecord TYPE integer USING nextval('id_Record_Seq'); ???

CLIENT_STATUS = ( ('0','Inativo'),('1','Ativo'))
class Client(models.Model):
    id = UuidField(primary_key=True)
    person = models.OneToOneField(Person)
    idRecord = models.CharField(max_length=15)
    legacyRecord = models.CharField(max_length=15)
    healthDocument = models.CharField(max_length=15)
    admission_date = models.DateField(null=True)
    referral_choice = models.ForeignKey(AdmissionReferral, null=True)
    indication_choice = models.ForeignKey(Indication, null=True)
    clientStatus = models.CharField(max_length=1, default='1', choices=CLIENT_STATUS)
    person_link = models.ManyToManyField(PersonLink)
    comments = models.TextField(blank=True)
    #history= audittrail.AuditTrail()

    def __unicode__(self):
        return u"%s" % self.person.name
    
    class Meta:
        ordering = ['person']
