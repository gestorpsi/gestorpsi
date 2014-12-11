from django.test import TestCase
from gestorpsi.users.views import *


class ScheduleTest(TestCase):

	def test_verify_email_is_blank(self):
		old_password = "123"
		email = ""
		email_confirmation = ""

		self.assertEquals(
			verify_requests(
				old_password,
				email,
				email_confirmation),
			"All fields are required")

	def test_verify_one_field_blank(self):
		old_password = "123"
		email = "test@test.com"
		email_confirmation = ""

		self.assertEquals(
			verify_requests(
				old_password,
				email,
				email_confirmation),
			"All fields are required")

	def test_different_emails(self):
		old_password = "123"
		email = "test@test.com"
		email_confirmation = "test_different@test.com"

		self.assertEquals(
			verify_requests(
				old_password,
				email,
				email_confirmation),
			"Confirmation does not match. Please try again")

	def test_correct_emails(self):
		old_password = "123"
		email = "test@test.com"
		email_confirmation = "test@test.com"

		self.assertEquals(
			verify_requests(
				old_password,
				email,
				email_confirmation),
			"")

	def test_blank_passwords(self):
		old_password = "123"
		password = ""
		password_confirmation = ""

		self.assertEquals(
			verify_requests(
				old_password,
				password,
				password_confirmation),
			"All fields are required")

	def test_different_passwords(self):
		old_password = "123"
		password = "1"
		password_confirmation = "12"

		self.assertEquals(
			verify_requests(
				old_password,
				password,
				password_confirmation),
			"Confirmation does not match. Please try again")

	def test_correct_passwords(self):
		old_password = "123"
		password = "12"
		password_confirmation = "12"

		self.assertEquals(
			verify_requests(
				old_password,
				password,
				password_confirmation),
			"")
