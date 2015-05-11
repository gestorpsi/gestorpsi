__author__ = 'levi'

from gestorpsi.phone.models import Phone, PhoneType
from gestorpsi.phone.views import *
import unittest

class PhoneTest(unittest.TestCase):
    phone = None
    def setup(self):
        self.phone = Phone()
        self.phone.phoneNumber = '81111111'
        self.phone.area = 'DF'

    def testIsEqual(self):
        self.assertFalse(is_equal(self.phone))

    def testPhoneList(self):

      '''  areas = [61, 62, 11]
        numbers = ['6787-2342', '8989-9889', '7907-8909']
        types = [1, 2, 3]

        phones = phone_list(ids=[None, None, None], exts=[None, None, None], areas=areas, numbers=numbers, types=types)
        for phone in phones:
            if (phone.area in areas) and (phone.phoneNumber in numbers):

                None
               #self.assertTrue(PhoneType.objects.get(1) == phone.phoneType)

    '''
      pass
    