"""
Copyright (C) 2008 GestorPsi

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

from django.test import TestCase
from .models import Profession, EducationalLevel
from gestorpsi.cbo.models import Occupation
from gestorpsi.client.models import Client


class ProfessionTest(TestCase):

    def setUp(self):
        self.occupation = Occupation(id=1,
                                     cbo_code="cbo_code", title="title")

        self.professiontest = Profession(
            profession=self.occupation, synonyms="synonyms",
            labor_market_status="labor", workplace="workplace",
            working_hours="working_hours", status=True, comments="comments")

        self.profession = self.occupation = "title"
        self.synonyms = "synonyms"
        self.labor_market_status = "labor"
        self.workplace = "workplace"
        self.working_hours = "working_hours"
        self.status = True
        self.comments = "comments"

    def testUnicode(self):
        self.assertEquals(self.profession, unicode(self.professiontest))
        self.assertEquals("synonyms", self.synonyms)
        self.assertEquals("labor", self.labor_market_status)
        self.assertEquals("workplace", self.workplace)
        self.assertEquals("working_hours", self.working_hours)
        self.assertEquals(True, self.status)
        self.assertEquals("comments", self.comments)


class EducationalLevelTest(TestCase):

    def setUp(self):

        self.educational_level = EducationalLevel(
            school_grade="School_Grade", comments="Comments")

        self.school_grade = "SCHOOL_GRADE"
        self.comments = "COMMENTS"

    def testUnicode(self):

        self.assertEquals(self.school_grade, unicode(self.school_grade))
        self.assertEquals("COMMENTS", self.comments)
