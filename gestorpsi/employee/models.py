# -*- coding: utf-8 -*-
from django.db import models
from gestorpsi.person.models import Person
from gestorpsi.util.uuid_field import UuidField
from gestorpsi.util import audittrail

class Employee(models.Model):
    id= UuidField(primary_key=True)
    person = models.OneToOneField(Person)
    hiredate = models.DateField(blank=True, null=True)
    job = models.CharField(max_length=30, blank=True)
    active = models.BooleanField(default=True)
    
    history= audittrail.AuditTrail()
    
    def __unicode__(self):
        return u"%s" % self.person.name
    class Meta:
        ordering = ['person']    