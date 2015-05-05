from django.contrib.auth.models import User
from gestorpsi.person.models import Person
from gestorpsi.organization.models import Organization
from gestorpsi.gcm.models.payment import PaymentType
from django.test import TestCase
import subprocess

# para usar request usar requestfactory do django que 
# esta dentro de django.test.client

class PersonEmptyTestCase(TestCase):
    def setUp(self):
		
        User.objects.create(username="user1", password="password")		
        user = User.objects.get(username="user1")
		
        Person.objects.create(user_id=user.id)
						      
        self.person = Person.objects.get(user_id=user.id)

	def tearDown(self):
	    for person in Person.objects.all():
	        person.delete()
	    
	    for user in User.objects.all():
	        user.delete()

    def testSaveNewPerson(self):
        self.assertEqual(Person.objects.all()[0], self.person,
                         "person has not been appropriately saved")
    
    def testGetAllPhones(self):
        self.assertEqual(self.person.get_phones(), '',
		                  "problem on getting phones from person")

    def testGetInternet(self):
        self.assertEqual(self.person.get_internet(), '', 
                         'problem on getting internet')
    
    def testGetDocuments(self):
        self.assertEqual(self.person.get_documents(), '',
                         'problem on getting user\'s documents')

    def testGetAddress(self):
        self.assertEqual(self.person.get_address(), '',
                         'problem on getting user\'s address')
                         
    def testGetFirstPhone(self):
        self.assertEqual(self.person.get_first_phone(), '',
                         "problem on getting user\'s  first phone")

    def testGetPhoto(self):
        files = subprocess.check_output(["locate", "male_generic_photo.png"]).split('\n')
        self.assertIn(self.person.get_photo(), files,
                      "problem on getting user's photo")

    def testGetBirthdate(self):
        self.assertEqual(self.person.get_birthdate(), '',
                         "problem on getting user's birthdate")

    def testGetBirthPlace(self):
        self.assertEqual(self.person.get_birth_place(), u"None - None",
                         "problem on getting user's birth place")

    def testGetFirstEmail(self):
        self.assertEqual(self.person.get_first_email(), '',
                         "problem on getting user's first email")

    def testGetFirstSite(self):
        self.assertEqual(self.person.get_first_site(), '',
                         "problem on getting user's first site")


class ActualPersonTestCase(TestCase):
    def setUp(self):
		
        User.objects.create(username="user1", password="password")		
        user = User.objects.get(username="user1")
		
        Person.objects.create(user_id=user.id)
						      
        self.person = Person.objects.get(user_id=user.id)

	def tearDown(self):
	    for person in Person.objects.all():
	        person.delete()
	    
	    for user in User.objects.all():
	        user.delete()
	        
    def testGetAge(self):
        pass
