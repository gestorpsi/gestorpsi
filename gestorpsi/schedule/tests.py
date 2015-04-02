from django.test import TestCase
from datetime import timedelta

# Determine which specific import should be done.
from gestorpsi.schedule.views import *


class ScheduleTest(TestCase):
    def test_start_time_less_than_end_time(self):
        start_time = timedelta(hours=8, minutes=30, seconds=0)
        end_time = timedelta(hours=9, minutes=30, seconds=0)

        self.assertEquals(times_are_invalid(start_time, end_time), False)

    def test_start_time_equal_to_end_time(self):
        start_time = timedelta(hours=8, minutes=30, seconds=0)
        end_time = timedelta(hours=8, minutes=30, seconds=0)

        self.assertEquals(times_are_invalid(start_time, end_time), True)

    def test_start_time_greater_than_end_time(self):
        start_time = timedelta(hours=9, minutes=30, seconds=0)
        end_time = timedelta(hours=8, minutes=30, seconds=0)

        self.assertEquals(times_are_invalid(start_time, end_time), True)

    def test_verify_client(self):

        self.assertEquals(verify_client(1), True)

        self.assertEquals(verify_client(23), True)

        self.assertEquals(verify_client(None), False)
