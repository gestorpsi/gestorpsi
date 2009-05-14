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
from django.utils.translation import ugettext as _
from gestorpsi.organization.models import Organization
from gestorpsi.place.models import Place, Room
from gestorpsi.util.uuid_field import UuidField

DURABILITY_TYPE= ( ('1',_('CONSUMABLE')), ('2', _('DURABLE')) )
"""
Devices are classified by their durability, thus this variable represents
the two kinds of durability type that are used to classify them.
"""

MOBILITY_TYPE= ( ( '1', _('FIX') ), ( '2', _('MOBILE') ) )
"""
Similarly, devices are also classified by their mobility, thus this variable represents
the two kinds of mobility type that are used to classify them.
"""

class DeviceDetailsManager(models.Manager):
    def mobile(self):
        return super(DeviceDetailsManager, self).get_query_set().filter(mobility__exact='2')
    
    def fix(self):
        return super(DeviceDetailsManager, self).get_query_set().filter(mobility__exact='1')

class DeviceType(models.Model):
    """
    This class represents device types.
    @version: 1.0
    """
    id= UuidField(primary_key=True)
    durability= models.CharField( max_length=1, choices=DURABILITY_TYPE )
    mobility= models.CharField( max_length=1, choices=MOBILITY_TYPE )
    restriction= models.CharField( max_length=100 )
    
    def __unicode__(self):
      return "durability: %s, mobility: %s, restriction: %s" % (self.print_durability(), self.print_mobility(), self.restriction)
  
    def print_durability(self):
       if self.durability == '1':
           return 'consumable'
       else:
           return 'durable'
   
    def print_mobility(self):
       if self.mobility == '1':
           return 'fix'
       else:
           return 'mobile'

class Device(models.Model):
    """
    The class C{Device} is used to represent devices in the context of the GestorPsi project. Using this class,
    the user is able to query the quantity of some kind of device currently available as well as the number of existing
    devices of the underlying type.
    @version: 1.0
    """
    id = UuidField(primary_key=True)
    description = models.CharField( max_length = 80 )
    organization = models.ForeignKey(Organization, null=True)

    def get_all_device_details(self):
        return DeviceDetails.objects.filter( device__id= self.id )

    def __unicode__(self):
       return u"%s" % ( self.description )

    def revision(self):
        return reversion.models.Version.objects.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision
   
    class Meta:
        ordering = ['description']


class DeviceDetails(models.Model):
    """
    Instances of this class holds details about devices. For example, brand, comments, and so forth.
    @version: 1.0
    @see: Device
    @see: DeviceType
    """
    id = UuidField(primary_key=True)
    brand = models.CharField( max_length=80 )
    model = models.CharField( max_length=80 )
    part_number = models.CharField( max_length=45 )
    lendable = models.BooleanField( default=True )
    comments = models.CharField( max_length=200 )
    
    durability = models.CharField( max_length=1, choices=DURABILITY_TYPE )
    prof_restriction = models.CharField( max_length=20, blank=True)
    mobility = models.CharField( max_length=1, choices=MOBILITY_TYPE )
    place = models.ForeignKey(Place, null=True)
    room = models.ForeignKey(Room, null=True)
    device = models.ForeignKey(Device)

    objects = DeviceDetailsManager()

    class Meta:
        ordering = ['brand']

    def __unicode__(self):
      return u"%s - %s" % (self.device.description, self.brand)

    def revision(self):
        return reversion.models.Version.objects.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision

reversion.register(DeviceDetails, follow=['device'])
reversion.register(Device)
