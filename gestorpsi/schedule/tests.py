from django.test import TestCase
from datetime import timedelta,datetime
import unittest

# Determine which specific import should be done.
from gestorpsi.schedule.views import *
from gestorpsi.schedule.models import *
from gestorpsi.address.models import Address
from gestorpsi.phone.models import Phone, PhoneType
from gestorpsi.place.models import PlaceType, Place, Room, RoomType
from gestorpsi.address.models import City, State, Country, AddressType


class ScheduleTest(unittest.TestCase):

    def setUp(self):
        self.schedule = ScheduleOccurrence()
        self.schedule.reserve = True
        self.schedule.annotation = "this is schedule test"
        self.schedule.start_time = datetime.now()
        self.schedule.end_time = datetime.now()

        self.place = Place(label='testing place')
        place_type = PlaceType(description='a place type')
        place_type.save()
        self.place.place_type = place_type
        phone_type = PhoneType(description='phone type test')
        self.phone = Phone(area='23', phoneNumber='45679078', ext='4444',
                      phoneType=phone_type)
        self.phone.content_object = self.place
        addressType = AddressType(description='Home')
        addressType.save()
        address = Address()
        address.addressPrefix = 'Rua'
        address.addressLine1 = 'Rui Barbosa, 1234'
        address.addressLine2 = 'Anexo II - Sala 4'
        address.neighborhood = 'Centro'
        address.zipCode = '12345-123'
        address.addressType = AddressType.objects.get(pk=1)
        country = Country(name='test', nationality='testing')
        country.save()
        state = State(name='test', shortName='t', country=country)
        state.save()
        city = City(name='test', state=state)
        city.save()
        address.city = city
        address.content_object = self.place
        self.place.save()
        self.room = Room()
        self.room.place = self.place
        room_type = RoomType()
        self.room.room_type = room_type
        self.room.furniture = "tree table"
        self.schedule.room = self.room


    def test_start_time_less_than_end_time(self):
        start_time = timedelta(hours=8, minutes=30, seconds=0)
        end_time = timedelta(hours=9, minutes=30, seconds=0)

        self.assertEquals(invalid_delta_time(start_time, end_time), False)

    def test_start_time_equal_to_end_time(self):
        start_time = timedelta(hours=8, minutes=30, seconds=0)
        end_time = timedelta(hours=8, minutes=30, seconds=0)
        self.assertEquals(invalid_delta_time(start_time, end_time), True)

    def test_start_time_greater_than_end_time(self):
        start_time = timedelta(hours=9, minutes=30, seconds=0)
        end_time = timedelta(hours=8, minutes=30, seconds=0)
        self.assertEquals(invalid_delta_time(start_time, end_time), True)

    def test_verify_client(self):
        self.assertEquals(verify_client(1), True)
        self.assertEquals(verify_client(23), True)
        self.assertEquals(verify_client(None), False)

    def test_is_past(self):
        self.assertEquals(self.schedule.is_past(), True)

    def test_was_confirmed(self):
        self.assertEquals(self.schedule.was_confirmed(), False)
    
    def test_have_session(self):
        self.assertEquals(self.schedule.have_session(), False)
        
    def test_schedule_occurrences(self):
        print schedule_occurrences()
        self.assertEquals(schedule_occurrences(),[])