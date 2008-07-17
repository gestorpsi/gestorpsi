from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Email(models.Model):
    email = models.EmailField(blank=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    def __unicode__(self):
        return self.email

class Site(models.Model):
    description = models.CharField(max_length=30, blank=True)
    site = models.URLField(blank=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    def __unicode__(self):
        return self.site

class IMNetwork(models.Model):
    description = models.CharField(max_length=30)
    def __unicode__(self):
        return self.description
    class Admin: pass

class InstantMessenger(models.Model):
    identity = models.CharField(max_length=50, blank=True)
    network = models.ForeignKey(IMNetwork, blank=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()    
    def __unicode__(self):
        return "%s (%s)" % (self.identity, self.network)