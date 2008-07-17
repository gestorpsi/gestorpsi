from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from gestorpsi.address.models import State

# deletar
ISSUER_CHOICES = (
    ('0','SSP'),
    ('1','DGPC'),
    ('2','SPTC'),
    ('3','MEX'),
    ('4','MAER'),
    ('5','MMA'),
    ('6','IFP'),
    ('7','SEDS'),
    ('8','PM'),
    ('9','CREA'),
    ('9','IIRGD'),
)

class Issuer(models.Model):
    description = models.CharField(max_length=30)
    def __unicode__(self):
        return self.description

class Document(models.Model):
    identityCard = models.CharField('Identity Card', max_length=15)
    issuer = models.ForeignKey(Issuer)
    state = models.ForeignKey(State)
    cpf = models.CharField('CPF', max_length=14)
    #Generic Relationship
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    def __unicode__(self):
        return "RG: %s / %s / %s\nCPF: %s" % (self.identityCard, self.issuer, self.state, self.cpf)