from django.db import models
from django.forms import ModelForm
from gestorpsi.address.models import Address
from gestorpsi.phone.models import Phone
from django.contrib.contenttypes import generic
from gestorpsi.organization.models import Organization
from django.contrib import admin

class PlaceType( models.Model ):
    """
    This class represents place types.
    @author: Vinicius H. S. Durelli
    @version: 1.0
    """
    description= models.CharField( max_length= 80 )
    
    def __unicode__(self):
        """
        Returns a representation of this place type as an unicode C{string}.
        """
        return "%s" % self.description
    
class PlaceTypeAdmin(admin.ModelAdmin):
    """
    I{This class was created only for testing purposes}
    """
    pass

admin.site.register(PlaceType, PlaceTypeAdmin)
    
class Place( models.Model ):
    """
    This class represents a place.
    @author: Vinicius H. S. Durelli
    @version: 1.0
    """
    label= models.CharField( max_length= 80 )
    visible= models.BooleanField(blank=True)
    address= generic.GenericRelation( Address )
    phones= generic.GenericRelation( Phone )
    place_type= models.ForeignKey( PlaceType )
    organization = models.ForeignKey(Organization, null= True, blank= True)

    def __unicode__(self):
       """
       Returns a representation of this place as an unicode C{string}.
       """
       return "%s" % self.label
    
    class Meta:
        ordering = ['label']
        
class PlaceAdmin(admin.ModelAdmin):
    """
    I{This class was created only for testing purposes}
    """
    pass

admin.site.register(Place, PlaceAdmin)

class RoomType( models.Model ):
   """
   This class contains information on room types, thus instances of this class can be used to
   handle information related to room types.
   @author: Vinicius H. S. Durelli
   @version: 1.0
   """
   description= models.CharField( max_length= 45, unique= True )
   
   """
   Returns a representation of this room type as an unicode C{string}.
   """
   def __unicode__(self):
      return "%s" % self.description

class RoomTypeAdmin(admin.ModelAdmin):
    """
    I{This class was created only for testing purposes}
    """
    pass

admin.site.register(RoomType, RoomTypeAdmin)

class Room( models.Model ):
   """
   This class represents a room, it also holds information on the furniture that belongs to
   the underlying room and its dimension.
   @author: Vinicius H. S. Durelli
   @version: 1.0
   """
   description= models.CharField( max_length= 80, blank=True )
   dimension= models.IntegerField(null=True, blank=True)
   place= models.ForeignKey( Place )
   room_type= models.ForeignKey( RoomType, related_name= 'room_type' )
   furniture= models.TextField()

   """
   Returns a representation of this room as an unicode C{string}.
   """
   def __unicode__(self):
      return "%s" % self.description

class RoomAdmin(admin.ModelAdmin):
    """
    I{This class was created only for testing purposes}
    """
    pass

admin.site.register(Room, RoomAdmin)

class RoomForm(ModelForm):
   class Meta:
      model= Room

class PlaceForm(ModelForm):
   class Meta:
       model= Place