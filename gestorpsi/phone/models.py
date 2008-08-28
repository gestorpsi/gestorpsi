# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib import admin
from gestorpsi.util import audittrail

class PhoneType(models.Model):
    """
    This class was created to represent phone types. Each phone type has
    a short description.
    @version: 1.0
    @see: Phone
    """
    description = models.CharField(max_length=20)
    def __unicode__(self):
        return self.description

class PhoneTypeAdmin(admin.ModelAdmin):
    pass

admin.site.register(PhoneType, PhoneTypeAdmin)

class Phone(models.Model):
    """
    This class holds information related to phone numbers.
    @version: 1.0
    @see: PhoneType
    """
    area = models.CharField('Area Code',max_length=2, core=True)
    phoneNumber = models.CharField('Phone Number', max_length=8, core=True)
    ext = models.CharField('Extension', max_length=4, blank=True)
    phoneType = models.ForeignKey(PhoneType)
    # Generic Relationship
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    
    history = audittrail.AuditTrail()
    
    def __cmp__(self, other):
        if (self.area == other.area) and \
           (self.phoneNumber == other.phoneNumber) and \
           (self.ext == other.ext) and \
           (self.phoneType == other.phoneType):
            return 0
        else:
            return 1
    
    def __unicode__(self):
        """
        Returns a representation of this phone number as a unicode C{string}; this C{string} follows the pattern:
        I{(area) phone-number}.
        """
        return "(%s) %s" % (self.area, self.phoneNumber)