from django.db import models
from gestorpsi.organization.models import Organization
from django.newforms import ModelForm

DURABILITY_TYPE= ( ('1','CONSUMABLE'), ('2', 'DURABLE') )
MOBILITY_TYPE= ( ( '1', 'FIX' ), ( '2', 'MOBILE' ) )

class DeviceType(models.Model):
    durability= models.CharField( max_length= 1, choices=DURABILITY_TYPE )
    mobility= models.CharField( max_length= 1, choices= MOBILITY_TYPE )
    restriction= models.CharField( max_length= 100 )
    
    def __unicode__(self):
        return "durability: %s, mobility: %s, restriction: %s" % (self.durability, self.mobility, self.restriction)
    
    class Admin:
        pass

class DeviceTypeForm(ModelForm):
      class Meta:
          model= DeviceType
    
class Device(models.Model):
    description= models.CharField( max_length= 80 )
    total_quantity= models.IntegerField()
    available_quantity= models.IntegerField()
    
    def __unicode__(self):
        return "description: %s, number of devices: %s, number of available devices: %s" % (self.description, self.total_quantity, self.available_quantity)
    
    class Admin:
        pass

class DeviceForm(ModelForm):
      class Meta:
          model= Device
    
class DeviceDetails(models.Model):
    brand= models.CharField( max_length= 80 )
    model= models.CharField( max_length= 80 )
    part_number= models.CharField( max_length= 45 )
    comments= models.CharField( max_length= 80 )
    device_type= models.ForeignKey( DeviceType, related_name= 'device_type' )
    device= models.ForeignKey( Device, related_name= 'device' )
    active = models.BooleanField(default=True)
        
    organization = models.ForeignKey(Organization, null=True)
    
    def __unicode__(self):
        return "brand: %s, model: %s, comments: %s" % (self.brand, self.model, self.comments)
    
    class Admin:
        pass

class DeviceDetailsForm(ModelForm):
      class Meta:
          model= DeviceDetails

"""
from gestorpsi.device.models import Device, DeviceDetails, DeviceType

#the line below creates a device type
device_type= DeviceType( durability= '1', mobility= '1', restriction= 'a restriction' )
device_type.save()
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
