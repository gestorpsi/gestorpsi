from gestorpsi.person.models import Person
from gestorpsi.careprofessional.models import InstitutionType, PostGraduate,\
    Profession

from django.test import TestCase


class InstitutionTypeTest(TestCase):
    def setUp(self):
        self.description = "description of the institution"
        self.institution = InstitutionType(
            description="description of the institution")

    def testUnicode(self):
        self.assertEquals(self.description, unicode(self.institution))


class PostGraduateTest(TestCase):
    def setUp(self):
        self.description = "description of the post graduate"
        self.post_graduate = PostGraduate(
            description="description of the post graduate")

    def testUnicode(self):
        self.assertEquals(self.description, unicode(self.post_graduate))


class ProfessionTest(TestCase):
    def setUp(self):
        self.type = "Doctor"
        self.profession = Profession

        self.profession.type = self.type

    def testUnicode(self):
        self.assertEquals(self.type, unicode(self.profession.type))


class ProfessionalProfile(TestCase):
    def setUp(self):
        self.professional_name = "Manuel"
        pass

    def testUnicode(self):
        # TODO: comparing the unicode of the class with the configured in
        #       setUp().
        pass
