from django.test import TestCase
from django.test.client import Client
from shobiz.utils import AppointmentManager
from shobiz.models import Store
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

class SessionTests(TestCase):
    ''' Tests that visiting pages returns appropriate session information '''

    def test_visit_index_view_creates_shobiz_session(self):
        ''' Creates a session containing (empty) appointment manager '''
        self.client = Client()
        response = self.client.get("/shobiz/")
        self.assertIsInstance(self.client.session['apt_manager'],\
                              AppointmentManager)


