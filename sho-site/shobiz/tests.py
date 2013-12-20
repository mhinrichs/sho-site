# -*- coding: utf-8 -*-

from django.test import TestCase
from django.test.client import Client
from shobiz.utils import AppointmentManager
from shobiz.models import Store, Employee
from datetime import datetime

class EmployeeWorkdayTests(TestCase):
    ''' TODO '''
    def test_blank_test(self):
        self.assertTrue(True)

class WorkdayCalendarTests(TestCase):
    ''' TODO '''
    def test_blank_test(self):
        self.assertTrue(True)

class AppointmentManagerTests(TestCase):

    def setUp(self):
        Store.objects.create(name = 'TheStore', \
                             romaji = 'TheStore', \
                             phone = '080-9999-9999', \
                             email = 'mail@mail.com', \
                             entry_date = datetime.now(), \
                             last_edited = datetime.now(), \
                             store_id = 's0001')
        Employee.objects.create(name = 'Uchimura Sho', \
                                romaji = 'Uchimura Sho', \
                                phone = '080-9999-9999', \
                                email = 'mail@mail.com', \
                                entry_date = datetime.now(), \
                                last_edited = datetime.now(), \
                                emp_id = 'e000001',
                                birthday = datetime.now())

    def test_empty_manager_is_empty(self):
        a = AppointmentManager()
        self.assertEqual(a.store, None)
        self.assertEqual(a.employee, None)
        self.assertEqual(a.cal_month, None)
        self.assertEqual(a.cal_year, None)
        self.assertEqual(a.target_date, None)
        self.assertEqual(a.target_time, None)

    def test_has_store_method(self):
        a = AppointmentManager()
        self.assertFalse(a.has_store())
        a.store = Store.objects.get(store_id = 's0001')
        self.assertTrue(a.has_store())

    def test_has_store_employee_method(self):
        a = AppointmentManager()
        self.assertFalse(a.has_store_employee())
        a.store = Store.objects.get(store_id = 's0001')
        a.employee = Employee.objects.get(emp_id = 'e000001')
        self.assertTrue(a.has_store_employee())

    def test_has_valid_year_month_method(self):
        a = AppointmentManager()
        #test None
        self.assertFalse(a.has_valid_year_month())
        #test year too high
        a.cal_year = 9999
        a.cal_month = 1
        self.assertFalse(a.has_valid_year_month())
        #test year too low
        a.cal_year = 1
        self.assertFalse(a.has_valid_year_month())
        #test month too high
        a.cal_year = 1980
        a.cal_month = 13
        self.assertFalse(a.has_valid_year_month())
        #test month too low
        a.cal_month = 0
        self.assertFalse(a.has_valid_year_month())
        #test strings values
        a.cal_year = "1980"
        a.cal_month = "4"
        self.assertFalse(a.has_valid_year_month())
        a.cal_year = "blah"
        a.cal_year = "blah"
        self.assertFalse(a.has_valid_year_month())
        #test 100 valid years
        for x in range(1955, 2056):
            for y in range(1, 13):
                a.cal_year = x
                a.cal_month = y
                self.assertTrue(a.has_valid_year_month())

class SessionTests(TestCase):
    ''' Tests that visiting pages returns appropriate session information '''

    def test_visit_index_view_creates_shobiz_session(self):
        ''' Creates a session containing (empty) appointment manager '''
        self.client = Client()
        response = self.client.get("/shobiz/")
        self.assertIsInstance(self.client.session['apt_manager'],\
                              AppointmentManager)

    def test_visiting_employee_without_apt_man_redirects(self):
        self.client = Client()
        response = self.client.get("/shobiz/employee/", follow=False)
        self.assertRedirects(response, "/shobiz/")

    def test_visiting_calendar_without_apt_man_redirects(self):
        self.client = Client()
        response = self.client.get("/shobiz/calendar/", follow=False)
        self.assertRedirects(response, "/shobiz/")


