from django.test import TestCase
from gestorpsi.users.views import *

class ScheduleTest(TestCase):

	def test_verify_email(self):
		email = ""
		email_confirmation = ""

		self.assertEquals(verify_emails(email, email_confirmation), "All fields are required")

		email = "test@test.com"
		email_confirmation = ""

		self.assertEquals(verify_emails(email, email_confirmation), "All fields are required")

		email = "test@test.com"
		email_confirmation = "test_different@test.com"

		self.assertEquals(verify_emails(email, email_confirmation), "email confirmation does not match. Please try again")

		email = "test@test.com"
		email_confirmation = "test@test.com"

		self.assertEquals(verify_emails(email, email_confirmation), "")
