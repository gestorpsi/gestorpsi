# -*- coding: utf-8 -*-

"""
Copyright (C) 2008 GestorPsi

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

import reversion
from django.db import models
from gestorpsi.address.models import Address
from gestorpsi.phone.models import Phone
from django.contrib.contenttypes import generic
from gestorpsi.organization.models import Organization
from gestorpsi.util.uuid_field import UuidField

class PlaceType( models.Model ):
    """
    This class represents place types.
    @version: 1.0
    """
    description= models.CharField( max_length= 100 )
    def __unicode__(self):
        return "%s" % self.description

class Place( models.Model ):
    """
    This class represents a place.
    @version: 1.0
    """
    id = UuidField(primary_key=True)
    label= models.CharField( max_length= 80 )
    visible= models.BooleanField(blank=True)
    address= generic.GenericRelation( Address )
    phones= generic.GenericRelation( Phone )
    place_type= models.ForeignKey( PlaceType )
    organization = models.ForeignKey(Organization, null= True, blank= True)
    
    def __unicode__(self):
       return "%s" % self.label
   
    def get_first_phone(self):
       if ( len( self.phones.all() ) != 0 ):
         return self.phones.all()[0]
       else:
         return ''
    
    class Meta:
        ordering = ['label']

    def revision(self):
        return reversion.models.Version.objects.get_for_object(self).latest('revision__date_created').revision

reversion.register(Place, follow=['address', 'phones'])

class RoomType( models.Model ):
   """
   This class contains information on room types, thus instances of this class can be used to
   handle information related to room types.
   @version: 1.0
   """
   description= models.CharField( max_length= 45, unique= True )

   def __unicode__(self):
      return "%s" % self.description

class Room( models.Model ):
   """
   This class represents a room, it also holds information on the furniture that belongs to
   the underlying room and its dimension.
   @version: 1.0
   """
   id = UuidField(primary_key=True)
   description= models.CharField( max_length= 80, blank=True )
   dimension= models.IntegerField(null=True, blank=True)
   place= models.ForeignKey( Place )
   room_type= models.ForeignKey( RoomType, related_name= 'room_type' )
   furniture= models.TextField()

   class Meta:
       ordering = ['description']

   def __unicode__(self):
      return "%s" % self.description

   def revision(self):
      return reversion.models.Version.objects.get_for_object(self).latest('revision__date_created').revision
  
   def __cmp__(self, other):
      if (self.description == other.description ) and \
         (self.dimension == other.dimension ) and \
         (self.room_type.id == other.room_type.id ) and \
         (self.furniture == other.furniture ):
         return 0
      else:
         return 1

reversion.register(Room)
