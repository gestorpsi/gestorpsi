from gestorpsi.person.models import Person
from gestorpsi.organization.models import Organization
from gestorpsi.users.models import User
from gestorpsi.careprofessional.models import InstitutionType, PostGraduate,\
    Profession, ProfessionalProfile, CareProfessional, LicenceBoard,\
    Availability, CareProfessionalManager

from django.test import TestCase


class InstitutionTypeTest(TestCase):
    def setUp(self):
        self.description = "description of the institution"
        self.institution = InstitutionType(
            description="description of the institution")

    def testUnicode(self):
        result = unicode(self.institution)
        expected_result = self.description

        self.assertEquals(result, expected_result)


class PostGraduateTest(TestCase):
    def setUp(self):
        self.description = "description of the post graduate"
        self.post_graduate = PostGraduate(
            description="description of the post graduate")

    def testUnicode(self):
        result = unicode(self.post_graduate)
        expected_result = self.description

        self.assertEquals(result, expected_result)


class ProfessionTest(TestCase):
    def setUp(self):
        self.type = "Doctor"
        self.profession = Profession

        self.profession.type = self.type

    def testUnicode(self):
        result = unicode(self.profession.type)
        expected_result = self.type

        self.assertEquals(result, expected_result)


class LicenceBoardTest(TestCase):
    def setUp(self):
        self.name = "licenses name"
        self.licences_board = LicenceBoard(name="licenses name")

    def testUnicode(self):
        result = unicode(self.licences_board)
        expected_result = self.name

        self.assertEquals(result, expected_result)


class StudentProfileTest(TestCase):
    def setUp(self):
        self.person = Person(name="tested person")
        self.care_professional_manager = CareProfessionalManager()

        self.availability = Availability()
        self.availability.day = "1"
        self.availability.hour = "2010-03-27"

        self.care_professional = CareProfessional(
            objects=self.care_professional_manager,
            availability=self.availability)
        #self.care_professional.person = self.person
        #self.care_professional.objects = self.care_professional_manager
        #self.care_professional.availability = self.availability

        self.professional = self.care_professional
        self.expected_professional = "tested person"

    def testUnicode(self):
        result = unicode(self.professional)
        expected_result = self.expected_professional

        self.assertEquals(result, expected_result)


class AvailabilityTest(TestCase):
    def setUp(self):
        self.expected_day_hour = "1 - 18:30"

        self.availability = Availability()
        self.availability.day = "1"
        self.availability.hour = "18:30"

    def testUnicode(self):
        result = unicode(self.availability)
        expected_result = self.expected_day_hour

        self.assertEquals(result, expected_result)


class CareProfessional(TestCase):
    def setUp(self):
        self.person = Person(name="tested person")
        self.care_professional_manager = CareProfessionalManager()

        self.availability = Availability
        self.availability.day = "1"
        self.availability.hour = "5"

        self.care_professional = CareProfessional(person=self.person,
            objects=self.care_professional_manager,
            availability=self.availability)
