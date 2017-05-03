# -*- coding: utf-8 -*-

from django.test import TestCase, Client
from django.contrib.auth.models import User, UserManager, Group
from django.core.urlresolvers import reverse

from gestorpsi.util.test_utils import user_stub, setup_required_data
from gestorpsi.service.models import Area, ServiceType, Service

class ServiceTests(TestCase):
    def setUp(self):
        self.client = Client()
        setup_required_data()
        self.forbidden_string = "We're sorry, but you dont have permissions to execute this operation."
        serv = ServiceType()
        serv.pk = 3
        serv.name = "Avaliação"
        serv.save()

    def test_service_should_redirect_unlogged_users(self):
        self.client.logout() # guarantee that the given user is signed out
        response = self.client.get(reverse('select_area'))
        self.assertEqual(response.status_code, 302)

    def test_service_should_show_forbidden_page_for_users_without_permission(self):
        self.client.post(reverse('registration-register'), user_stub())
        res = self.client.login(username=user_stub()["username"], password=user_stub()["password1"])
        response = self.client.get(reverse('select_area'))
        self.assertEqual(self.forbidden_string in response.content, True)

    def test_service_should_work_for_logged_users(self):
        self.client.post(reverse('registration-register'), user_stub())
        res = self.client.login(username=user_stub()["username"], password=user_stub()["password1"])
        user = User.objects.get(username=user_stub()["username"])
        user.is_superuser = True
        user.save()
        response = self.client.get(reverse('select_area'))
        self.assertEqual(self.forbidden_string in response.content, False)

    def test_service_creation_should_work_for_correct_values(self):
        self.client.post(reverse('registration-register'), user_stub())
        self.cl.login(
            username=user_stub()["username"],
            password=user_stub()["password1"]
        )
        print("LOGIN FUNFOU YEAH")
        user = User.objects.get(username=user_stub()["username"])
        print("USER => ", user)
        area = Area(area_name='forensic', area_code='forensic')
        area.save()
        old_service_count = Service.objects.all().count()
        user.is_superuser = True
        user.save()
        res = self.client.get(reverse('select_area'))
        self.assertEqual('forensic' in res.content, True)
        res = self.client.post(reverse('service_form'), {'area': area.area_code})
        service_fixture = {
            'service_name': 'nice_service',
            'service_area': '1',
            'service_type': '3',
            'service_color': 'cafef3',
            'service_profession': '1',
            'service_description': 'a nice service',
            'service_keywords': 'hello',
            'research_project_name': u'',
            'comments': u''
        }
        res = self.client.post(reverse('save_service'), service_fixture)
        new_service_count = Service.objects.all().count()
        self.assertEqual(new_service_count, old_service_count+1)

    def test_service_should_not_create_for_invalid_values(self):
        self.client.post(reverse('registration-register'), user_stub())
        self.client.login(username=user_stub()["username"], password=user_stub()["password1"])
        area = Area(area_name='forensic', area_code='forensic')
        area.save()
        old_service_count = Service.objects.all().count()
        user = User.objects.get(username=user_stub()["username"])
        user.is_superuser = True
        user.save()
        res = self.client.get(reverse('select_area'))
        self.assertEqual('forensic' in res.content, True)
        res = self.client.post(reverse('service_form'), {'area': area.area_code})
        service_fixture = {
            'service_name': '',
            'service_area': '1',
            'service_type': '3',
            'service_color': 'cafef3',
            'service_profession': '1',
            'service_description': 'a nice service',
            'service_keywords': 'hello',
            'research_project_name': u'',
            'comments': u''
        }
        res = self.client.post(reverse('save_service'), service_fixture)
        new_service_count = Service.objects.all().count()
        self.assertEqual(new_service_count, old_service_count)
