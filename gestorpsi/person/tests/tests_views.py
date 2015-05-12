from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from gestorpsi.person.models import Person
from gestorpsi.person.views import person_save, person_type_url
from gestorpsi.client.models import Client
from gestorpsi.internet.models import EmailType, Email, Site
from django.test import TestCase, RequestFactory


class TestPersonView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        p = Person()

        User.objects.create(username="user1", password="password")      
        p.user = User.objects.get(username="user1")

        p.save()

        client = Client(person=p, idRecord=1)
        client.save()

        self.person = Person.objects.get(user_id=p.user.id)

    def testPersonTypeURL(self):
        client = self.person.client
        returned_url = person_type_url(self.person)
        expected_url = "/client/%s/" % client.id
        self.assertEqual(returned_url, expected_url)