from django.db import models
from django.newforms import ModelForm

class Client(models.Model): 
    name = models.CharField('Complete Name', max_length=200, help_text='Put your full name', core=True)
    email = models.EmailField('e-mail')
    birthDate = models.DateField('Birthdate', core=True)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']
    class Admin:
        pass

class ClientForm(ModelForm):
    class Meta:
        model = Client

class Phone(models.Model):
    area = models.CharField('Area Code',max_length=2, core=True)
    phoneNumber = models.CharField('Phone Number', max_length=8, core=True)
    ext = models.CharField('Extension', max_length=4, blank=True)
    client = models.ForeignKey(Client, edit_inline=models.TABULAR, num_in_admin=1)
    def __unicode__(self):
        return "(%s) %s" % (self.area, self.phoneNumber)
    class Admin:
        pass

class PhoneForm(ModelForm):
    class Meta:
        model = Phone
        exclude = ('client')