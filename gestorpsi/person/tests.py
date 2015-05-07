from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from gestorpsi.person.models import Person
from gestorpsi.internet.models import EmailType, Email, Site
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
        self.assertEqual(Person.objects.all()[0], self.person)
    
    def testGetAllPhones(self):
        self.assertEqual(self.person.get_phones(), '')

    def testGetInternet(self):
        self.assertEqual(self.person.get_internet(), '')
    
    def testGetDocuments(self):
        self.assertEqual(self.person.get_documents(), '')

    def testGetAddress(self):
        self.assertEqual(self.person.get_address(), '')
                         
    def testGetFirstPhone(self):
        self.assertEqual(self.person.get_first_phone(), '')

    def testGetPhoto(self):
        files = subprocess.check_output(["locate", "male_generic_photo.png"]).split('\n')
        self.assertIn(self.person.get_photo(), files)

    def testGetBirthdate(self):
        self.assertEqual(self.person.get_birthdate(), '')

    def testGetBirthPlace(self):
        self.assertEqual(self.person.get_birth_place(), u"None - None")

    def testGetFirstEmail(self):
        self.assertEqual(self.person.get_first_email(), '')

    def testGetFirstSite(self):
        self.assertEqual(self.person.get_first_site(), '')


class ActualPersonTestCase(TestCase):
    def setUp(self):
        person = Person()
		
        User.objects.create(username="user1", password="password")		
        person.user = User.objects.get(username="user1")
	    
        person.birthDate = "1990-05-14"
        person.birthForeignCity = "Melbourne"
        person.birthForeignState = "Victoria"
        person.birthForeignCountry = '1'
        
        person.save()
        
        contentType = ContentType()
        contentType.app_label = "auth"
        contentType.model = "any"
        contentType.save()
        
        emailType = EmailType()
        emailType.description = "Email Type"
        emailType.save()
        email = Email()
        email.email = "email@email.com"
        email.email_type = EmailType.objects.all()[0]
        email.content_object = person
        email.save()

        site = Site()
        site.description = "this is a website"
        site.site = "www.google.com.br"
        site.content_object = person
        site.save()

        person.save()

        self.p = Person.objects.get(user_id=person.user.id)

	def tearDown(self):
	    for person in Person.objects.all():
	        person.delete()

	    for user in User.objects.all():
	        user.delete()

    def testGetActualBirthdate(self):
        self.assertEqual(self.p.get_birthdate(), "14/05/1990")

    def testGetActualBirthPlace(self):
        self.assertEqual(self.p.get_birth_place(), "Melbourne - Victoria")

    def testGetActualFirstEmail(self):
        self.assertEqual(self.p.get_first_email().email, "email@email.com")

    def testGetActualSite(self):
        self.assertEqual(self.p.get_first_site().site, "www.google.com.br")

    def testGetAge(self):
        self.assertEqual(self.p.get_age(), 24)

    def testGetInternet(self):
        text = "E-mail: email@email.com | Web Page: www.google.com.br"
        self.assertEqual(self.p.get_internet(), text)
