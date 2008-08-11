from django.db import models
from gestorpsi.person.models import Person

class PersonLink(models.Model):
    person = models.OneToOneField(Person)
    relation = models.CharField(max_length=10)
    responsible = models.BooleanField(default=False)
    def __unicode__(self):
        return u"%s" % self.person.firstName

CLIENT_STATUS = ( ('0','Inativo'),('1','Ativo'))
class Client(models.Model):
    person = models.OneToOneField(Person)
    idRecord = models.CharField(max_length=10)
    legacyRecord = models.CharField(max_length=10)
    healthDocument = models.CharField(max_length=10)
    indication = models.CharField(max_length=10)
    clientStatus = models.CharField(max_length=1, default = '1', choices=CLIENT_STATUS)
    personLink = models.ManyToManyField(PersonLink)
    
    #active = models.BooleanField(default=True)
    
    def __unicode__(self):
        return u"%s" % self.person.name
    
    class Meta:
        ordering = ['person']

"""
Testes do Models no shell de Cliente e seus vinculos

from gestorpsi.person.models import Person
from gestorpsi.client.models import Client, PersonLink

# Seleciona algumas pessoas ja existentes
p1 = Person.objects.get(pk=1)
p2 = Person.objects.get(pk=2)
p3 = Person.objects.get(pk=3)

# Cria um Cliente
c = Client()
c.idRecord = '1234'
c.legacyRecord = '1234'
c.healthDocument = '1234'
c.indication = 'ninguem'
c.clientStatus = 'ativo'
c.person = p1
c.save()

# Cria o primeiro vinculo
l1 = PersonLink()
l1.relation = 'pai'
l1.responsible = True
l1.person = p2
l1.save()

# Cria o segundo vinculo
l2 = PersonLink()
l2.relation = 'mae'
l2.responsible = True
l2.person = p3
l2.save()

# Nao precisa chamar save()
c.personLink.add(l1)
c.personLink.add(l2)

# Lista todos os vinculos do Cliente
from gestorpsi.client.models import Client
c = Client.objects.get(pk=1)
c.personLink.all()

# Lista quem esta vinculado a uma pessoa X
from gestorpsi.client.models import PersonLink
p = PersonLink.objects.get(pk=1)
p.client_set.all()

"""