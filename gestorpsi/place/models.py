from django.db import models
from django.forms import ModelForm
from gestorpsi.address.models import Address
from gestorpsi.phone.models import Phone
from django.contrib.contenttypes import generic
from gestorpsi.organization.models import Organization

class PlaceType( models.Model ):
    description= models.CharField( max_length= 80 )
    
    def __unicode__(self):
        return "%s" % self.description
    
    class Admin:
        pass
    
class Place( models.Model ):
   label= models.CharField( max_length= 80 )
   visible= models.BooleanField(blank=True)
   address= generic.GenericRelation( Address )
   phones= generic.GenericRelation( Phone )
   place_type= models.ForeignKey( PlaceType )
   organization = models.ForeignKey(Organization, null= True, blank= True)

   def __unicode__(self):
      return "%s" % self.label

   class Admin:
      pass

class RoomType( models.Model ):
   description= models.CharField( max_length= 45, unique= True )
   
   def __unicode__(self):
      return "%s" % self.description

   class Admin:
      pass

class Room( models.Model ):
   description= models.CharField( max_length= 80, blank=True )
   dimension= models.IntegerField(null=True, blank=True)
   place= models.ForeignKey( Place )
   room_type= models.ForeignKey( RoomType, related_name= 'room_type' )
   furniture= models.TextField()

   def __unicode__(self):
      return "%s" % self.description

   class Admin:
      pass
  
class RoomForm(ModelForm):
      class Meta:
          model= Room

class PlaceForm(ModelForm):
    class Meta:
        model= Place