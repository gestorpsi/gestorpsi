# -*- coding: utf-8 -*-

from django.db import models
from django.forms import ModelForm
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib import admin
from gestorpsi.util import audittrail

class EmailType(models.Model):
    description= models.CharField( max_length= 45 )
    def __unicode__(self):
        return self.description

class EmailTypeAdmin(admin.ModelAdmin):
    pass

admin.site.register(EmailType, EmailTypeAdmin)

class Email(models.Model):
    email = models.EmailField(blank=True)
    email_type = models.ForeignKey( EmailType )
    # Generic Relation
    content_type= models.ForeignKey(ContentType)
    object_id= models.PositiveIntegerField()
    content_object= generic.GenericForeignKey()

    history = audittrail.AuditTrail()

    def __cmp__(self, other):
        if (self.email == other.email) and \
           (self.email_type == other.email_type):
            return 0
        else:
            return 1

    def __unicode__(self):
        return self.email

class EmailForm(ModelForm):
    class Meta:
        model= Email

class Site(models.Model):
    description = models.CharField(max_length=30, blank=True)
    site = models.URLField(blank=True)
    # Generic Relation
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    history = audittrail.AuditTrail()

    def __cmp__(self, other):
        if (self.description == other.description) and \
           (self.site == other.site):
            return 0
        else:
            return 1    
    
    def __unicode__(self):
        return self.site

class IMNetwork(models.Model):
    description = models.CharField(max_length=30)
    def __unicode__(self):
        return self.description

class IMNetworkAdmin(admin.ModelAdmin):
    pass

admin.site.register(IMNetwork, IMNetworkAdmin)

class InstantMessenger(models.Model):
    identity = models.CharField(max_length=50, blank=True)
    network = models.ForeignKey(IMNetwork, blank=True)
    # Generic Relation
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    
    history = audittrail.AuditTrail()

    def __cmp__(self, other):
        if (self.identity == other.identity) and \
           (self.network == other.network):
            return 0
        else:
            return 1

    def __unicode__(self):
        return "%s (%s)" % (self.identity, self.network)