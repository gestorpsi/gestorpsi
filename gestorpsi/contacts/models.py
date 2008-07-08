from django.db import models

# Create your models here.
gender_list = (('M','Male'),('F','Female'))

class Establishment(models.Model):
    name = models.CharField('name',max_length=100)
    email = models.EmailField('Email')
    site = models.URLField('site', max_length=50)    
    def __unicode__(self):
        return self.name    
    
    class Admin:
        pass


class CareProfessional(models.Model):
    name = models.CharField('name',max_length=100, core=True)
    gender = models.CharField(max_length=1, choices=gender_list)    
    establishment = models.ForeignKey(Establishment, edit_inline = models.TABULAR, num_in_admin=1)
    def __unicode__(self):
        return self.name        


    
    
   
