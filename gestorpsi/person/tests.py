from django.contrib.auth.models import User
from gestorpsi.person.models import Person
from gestorpsi.organization.models import Organization
from gestorpsi.gcm.models.payment import PaymentType
import unittest2

# para usar request usar requestfactory do django que 
# esta dentro de django.test.client

class PersonTestCase(unittest2.TestCase):
	def setUp(self):
		
		User.objects.create(username="user", password="password")		
		user = User.objects.get(username="user")
		
		Person.objects.create(user_id=user.id)
						      
		self.person = Person.objects.get(user_id=user.id)

	def testSaveNewPerson(self):
		self.assertEqual(Person.objects.all()[0], self.person,
					 "person has not been appropriately saved")
