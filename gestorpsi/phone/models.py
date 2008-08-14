from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib import admin

class PhoneType(models.Model):
    description = models.CharField(max_length=20)
    def __unicode__(self):
        return self.description

class PhoneTypeAdmin(admin.ModelAdmin):
    pass

admin.site.register(PhoneType, PhoneTypeAdmin)

class Phone(models.Model):
    area = models.CharField('Area Code',max_length=2, core=True)
    phoneNumber = models.CharField('Phone Number', max_length=8, core=True)
    ext = models.CharField('Extension', max_length=4, blank=True)
    phoneType = models.ForeignKey(PhoneType)
    # Generic Relationship
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    def __unicode__(self):
        return "(%s) %s" % (self.area, self.phoneNumber)