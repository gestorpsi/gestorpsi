from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Country(models.Model):
    name = models.CharField(max_length=50)
    nationality = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']

class State(models.Model):
    name = models.CharField(max_length=50)
    shortName = models.CharField(max_length=2)
    country = models.ForeignKey(Country)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']

class City(models.Model):
    name = models.CharField(max_length=50)
    state = models.ForeignKey(State)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']

class AddressType(models.Model):
    description = models.CharField(max_length=20)
    def __unicode__(self):
        return self.description
    class Admin: pass

class Address(models.Model):
    # Falta colocar NUMERO da casa
    addressPrefix = models.CharField(max_length=10)
    addressLine1 = models.CharField(max_length=50)
    addressLine2 = models.CharField(max_length=50)
    neighborhood = models.CharField(max_length=30)
    zipCode = models.CharField(max_length=10)
    addressType = models.ForeignKey(AddressType)
    city = models.ForeignKey(City)
    # Generic Relationship
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    def __unicode__(self):
        return "%s %s\n%s" % (self.addressPrefix, self.addressLine1, self.addressLine2)