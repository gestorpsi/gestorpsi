from django.db import models
from django.newforms import ModelForm
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

PHONETYPE_CHOICES = (('0','Home'),('1','Work'),('2','Mobile'),('3','FAX'))

class Phone(models.Model):
    # Fields
    area = models.CharField('Area Code',max_length=2, core=True)
    phoneNumber = models.CharField('Phone Number', max_length=8, core=True)
    ext = models.CharField('Extension', max_length=4, blank=True)
    phoneType = models.CharField('Phone Type',max_length=1, choices=PHONETYPE_CHOICES)
    
    # Generic Relationship
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    def __unicode__(self):
        return "(%s) %s" % (self.area, self.phoneNumber)
#    class Admin:
#        pass

#class PhoneForm(ModelForm):
#    class Meta:
#        model = Phone
#        exclude = ('client')
