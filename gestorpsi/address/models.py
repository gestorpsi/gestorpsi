from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Country(models.Model):
    name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']

class State(models.Model):
    name = models.CharField(max_length=100)
    shortName = models.CharField(max_length=2)
    country = models.ForeignKey(Country)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']

class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']

addressType_list = (('0','HOME'), ('1','WORK'), ('2','MAIL_ONLY'))
class Address(models.Model):
    addressPrefix = models.CharField(max_length=10)
    addressLine1 = models.CharField(max_length=100)
    addressLine2 = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)
    zipCode = models.CharField(max_length=10)
    addressType = models.CharField(max_length=1, choices=addressType_list)
    city = models.ForeignKey(City)
    # Generic Relationship
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()