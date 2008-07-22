from django.db import models
from gestorpsi.person.models import Person

class Employee(models.Model):
    person = models.OneToOneField(Person)
    hiredate = models.DateField()
    job = models.CharField(max_length=30)
    def __unicode__(self):
        return u"%s" % self.person.firstName