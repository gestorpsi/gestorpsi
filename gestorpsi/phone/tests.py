__author__ = 'levi'

from gestorpsi.phone.models import Phone
import unittest

class PhoneTest(unittest.TestCase):
    def setup(self):
        self.phone = Phone()
        self.phone.phoneNumber = '81111111'
        self.phone.area = 'DF'

    def testCompareNumbers(self):
        self.assertEqual(self.phone.__cmp__(self.phone.phoneNumber,'81111111'), 1)
