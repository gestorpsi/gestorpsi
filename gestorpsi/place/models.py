from django.db import models
from django.newforms import ModelForm
import unittest

class Address( models.Model ):
   street= models.CharField( max_length= 200 )
   city= models.CharField( max_length= 80 )

   def __unicode__(self):
      return "Street: %s, City: %s" % ( self.street, self.city )

   class Admin:
      pass


class Place( models.Model ):
   description= models.CharField( max_length= 80 )
   visible= models.BooleanField()
   address= models.ForeignKey( Address ) 

   def __unicode__(self):
      return "%s" % self.description
  
   class Meta:
       ordering = ['address']

   class Admin:
      pass

class PlaceForm(ModelForm):
    class Meta:
        model= Place


class RoomType( models.Model ):
   description= models.CharField( max_length= 45, unique= True )
   
   def __unicode__(self):
      return "%s" % self.description

   class Admin:
      pass


class Room( models.Model ):
   description= models.CharField( max_length= 80 )
   size= models.IntegerField()
   place= models.ForeignKey( Place, related_name= 'place' )
   room_type= models.ForeignKey( RoomType, related_name= 'room_type' )

   def __unicode__(self):
      return "%s" % self.description

   class Admin:
      pass
  
class RoomForm(ModelForm):
      class Meta:
          model= Room

