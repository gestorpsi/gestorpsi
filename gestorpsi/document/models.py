from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from gestorpsi.address.models import State
from django.contrib import admin

class Issuer(models.Model):
    description = models.CharField(max_length=30)
    def __unicode__(self):
        return u"%s" % self.description

class IssuerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Issuer, IssuerAdmin)

class TypeDocument(models.Model):
    description = models.CharField(max_length=30)
    mask = models.CharField(max_length=30, blank=True)
    def __unicode__(self):
        return u"%s" % self.description

class TypeDocumentAdmin(admin.ModelAdmin):
    pass

admin.site.register(TypeDocument, TypeDocumentAdmin)


class Document(models.Model):
    typeDocument = models.ForeignKey(TypeDocument)
    document = models.CharField(max_length=50)
    issuer = models.ForeignKey(Issuer, null=True, blank=True)
    state = models.ForeignKey(State, null=True, blank=True)
    
    #Generic Relationship
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    def __unicode__(self):
        return u"%s: %s / %s - %s" % (self.typeDocument, self.document, self.issuer, self.state)