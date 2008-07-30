from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from gestorpsi.address.models import State

class Issuer(models.Model):
    description = models.CharField(max_length=30)
    def __unicode__(self):
        return u"%s" % self.description
    class Admin: pass

class TypeDocument(models.Model):
    description = models.CharField(max_length=30)
    mask = models.CharField(max_length=30)
    def __unicode__(self):
        return u"%s" % self.description
    class Admin: pass

class Document(models.Model):
    typeDocument = models.ForeignKey(TypeDocument)
    document = models.CharField(max_length=50)
    issuer = models.ForeignKey(Issuer)
    state = models.ForeignKey(State, null=True)
    
    #Generic Relationship
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    def __unicode__(self):
        return u"RG: %s / %s / %s\nCPF: %s" % (self.identityCard, self.issuer, self.state, self.cpf)