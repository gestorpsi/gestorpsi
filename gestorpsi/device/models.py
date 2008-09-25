# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm
from gestorpsi.organization.models import Organization
from gestorpsi.place.models import Room
from gestorpsi.careprofessional.models import Profession
from gestorpsi.util.uuid_field import UuidField
from gestorpsi.util import audittrail


DURABILITY_TYPE= ( ('1','CONSUMABLE'), ('2', 'DURABLE') )
"""
Devices are classified by their durability, thus this variable represents
the two kinds of durability type that are used to classify them.
"""

MOBILITY_TYPE= ( ( '1', 'FIX' ), ( '2', 'MOBILE' ) )
"""
Similarly, devices are also classified by their mobility, thus this variable represents
the two kinds of mobility type that are used to classify them.
"""

class DeviceType(models.Model):
    """
    This class represents device types.
    @author: Vinicius H. S. Durelli
    @version: 1.0
    """
    id= UuidField(primary_key=True)
    durability= models.CharField( max_length= 1, choices= DURABILITY_TYPE )
    mobility= models.CharField( max_length= 1, choices= MOBILITY_TYPE )
    restriction= models.CharField( max_length= 100 )
    
    def __unicode__(self):
      """
      Returns a representation of this device type as an unicode C{string}.
      """
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
    @author: Vinicius H. S. Durelli
    @version: 1.0
    """
    id= UuidField(primary_key=True)
    description= models.CharField( max_length= 80 )
    
    organization = models.ForeignKey(Organization, null=True)
    
    history= audittrail.AuditTrail()
    
    def __unicode__(self):
       """
       Returns a representation of this device as an unicode C{string}.
       """
       return "description: %s" % ( self.description )
    """
    Returns a list of all related device details 
    """
    def get_all_device_details(self):
        return DeviceDetails.objects.filter( device__id= self.id )


class DeviceDetails(models.Model):
    """
    Instances of this class holds details about devices. For example, brand, comments, and so forth.
    @author: Vinicius H. S. Durelli
    @version: 1.0
    @see: Device
    @see: DeviceType
    """
    id = UuidField(primary_key=True)
    brand = models.CharField( max_length=80 )
    model = models.CharField( max_length=80 )
    part_number = models.CharField( max_length=45 )
    durability = models.CharField( max_length=1, choices=DURABILITY_TYPE )
    lendable = models.BooleanField( default=True )
    restriction = models.ManyToManyField( Profession, null=True, blank=True)
    room = models.ForeignKey( Room, related_name='room', null=True )
    device = models.ForeignKey( Device, related_name='device' )
    comments = models.CharField( max_length=200 )

    def __unicode__(self):
      """
      Returns a representation of the details related to a particular device as an unicode C{string}.
      """
      return u"%s - %s" % (self.brand, self.model)

class DeviceTypeForm(ModelForm):
      class Meta:
          model= DeviceType

class DeviceForm(ModelForm):
      class Meta:
          model= Device

class DeviceDetailsForm(ModelForm):
      class Meta:
          model= DeviceDetails

"""
from gestorpsi.device.models import Device, DeviceDetails, DeviceType

#the line below creates a device type
device_type= DeviceType( durability= '1', mobility= '1', restriction= 'a restriction' )
device_type.save()list_of_dev_details= DeviceDetails.objects.all().filter( device= device.id )
DeviceType.objects.all()

#the line below shows how to create and save an instance of the class Device
device= Device( description= "camera", total_quantity= 4, available_quantity= 4 )
device.save()
Device.objects.all()

#the lines below create many device details and save them
device_details1= DeviceDetails( brand= 'sony', model= '500', part_number= 'X41897CVw', comments= 'comments', device_type= DeviceType.objects.get(pk=1), device= device )
device_details1.save()

device_details2= DeviceDetails( brand= 'panasonic', model= 'XF4000', part_number= 'RYTH345t', comments= 'comments', device_type= DeviceType.objects.get(pk=1), device= device )
device_details2.save()

device_details3= DeviceDetails( brand= 'LG', model= 'cyber-4550', part_number= 'FEWASEF', comments= 'comments', device_type= DeviceType.objects.get(pk=1), device= device )
device_details3.save()

#retrieves a list of all 'device details' related to the 'device' with id code equal to 1
DeviceDetails.objects.filter( device__exact= 1)

list_device_details= DeviceDetails.objects.filter( device__exact= device.id )
for device_details in list_device_details:
   print device_details.device_type

"""