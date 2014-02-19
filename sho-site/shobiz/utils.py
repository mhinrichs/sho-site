# -*- coding: utf-8 -*-

from django.core.mail import send_mail
from django.template.loader import render_to_string
from datetime import date, datetime
from calendar import Calendar
from shobiz.models import Workday
from shobiz.validators import valid_session_for_view

class EmployeeWorkday:

    def __init__(self, store, employee, dateobject, workday=None, status=None):
        self.store = store
        self.employee = employee
        self.date = dateobject
        self.workday = workday
        self.status = status

    def pair_workday(self, query_set):
        for entry in query_set:
            if self.status == 'dimmed': #ignore records outside of the current month
                pass
            elif entry.date == self.date:
                self.workday = entry
                self.status = entry.get_status()
        if self.status == None: # None as status means no workday record / employee is off work
            self.status = 'offwork'

    def to_string(self):
        return self.date.strftime("%Y_%m_%d") #underscores because its used as an id in html tag

class WorkdayCalendar:

    '''Pairs workdays with calendar from the calendar module.
       The workdays are captured as a single query set to avoid hitting
       the database more than once.'''

    def __init__(self, weekdaystart = 6):
        self.calendar = Calendar(weekdaystart)

    def create_calendar(self, apt_man):
        ''' Gets a queryset containing workdays from the database.
            Pairs queryset with dates from the python calendar module
            and returns a new monthdatescalendar with the dates replaced
            with EmployeeWorkday objects.

            The status of the day (how many of the timeblocks are booked)
            is updated during the pairing process. '''
        store = apt_man.store
        employee = apt_man.employee
        year = apt_man.cal_year
        month = apt_man.cal_month
        query_set = Workday.by_store_emp_year_month(store, employee, year, month)
        calendar = []
        for week in self.calendar.monthdatescalendar(year, month):
            workweek = []
            for date in week:
                if date.month != month: #process status for other months (dimmed)
                    workday = EmployeeWorkday(store, employee, date, None, 'dimmed')
                    workday.pair_workday(query_set)
                else:  #process the date and match queries from the database
                    workday = EmployeeWorkday(store, employee, date)
                    workday.pair_workday(query_set)
                workweek.append(workday)
            calendar.append(workweek)
        return calendar

    def get_weekdays(self):
        ''' Todo optionally add weekdays for non japan regions
            by adding an interface with the locale module.
            Right now these are just the weekdays in Japanese.'''
        return [r"日", r"月", r"火", r"水", r"木", r"金", r"土"]

    def get_calendar_context(self, request):
        '''Gets an appropriate context for a calendar based off of
           a client sesssion'''
        context = {}
        if valid_session_for_view(request, 'calendar') and \
        request.session['apt_manager'].has_valid_year_month():
            apt_man = request.session['apt_manager']
            context['days_of_week'] = self.get_weekdays()
            context['store'] = apt_man.store
            context['employee'] = apt_man.employee
            context['year'] = apt_man.cal_year
            context['month'] = apt_man.cal_month
            context['calendar'] = self.create_calendar(apt_man)
        else:
            raise ValueError
        return context

    def navigate(self, request):
        ''' Updates session and returns a new calendar
            based on an ajax request. '''
        if not valid_session_for_view(request, 'calendar') or \
           not request.session['apt_manager'].has_valid_year_month():
            raise ValueError

        apt_man = request.session['apt_manager']
        store, employee = apt_man.store, apt_man.employee
        year, month = apt_man.cal_year, apt_man.cal_month
        action = request.GET['action']

        #navigation functions
        def current():
            d = datetime.now()
            apt_man.cal_year = d.year
            apt_man.cal_month = d.month

        def back():
            if month > 1:
                apt_man.cal_month = month - 1
            else:
                apt_man.cal_year = year - 1
                apt_man.cal_month = 12

        def forward():
            if month < 12:
                apt_man.cal_month = month + 1
            else:
                apt_man.cal_month = 1
                apt_man.cal_year = year + 1

        def move(action):
            actions = {'current': current,
                       'back': back,
                       'forward': forward}
            try:
                return actions[action]()
            except KeyError:
                return actions['current']()
            request.session['apt_manager'] = apt_man

        return move(action)

    def get_schedule_context(self, request):
        context = {}
        if valid_session_for_view(request, 'schedule'):
            store = request.session['apt_manager'].store
            employee = request.session['apt_manager'].employee
            date = request.session['apt_manager'].target_date
            workday = Workday.by_store_emp_date(store, employee, date)
            context['year'] = date.year
            context['month'] = date.month
            context['workday'] = workday
            context['store'] = store
            context['employee'] = employee
        else:
            raise ValueError("Insufficient session data to create schedule context")
        return context

    def encode_datestr(self, datestring):
        ''' encodes a datestr to a datetime object '''
        try:
            date = datetime.strptime(datestring, '%Y_%m_%d')
        except:
            raise ValueError("Must follow the format YYYY_M_D")
        return date

class AppointmentManager:
    ''' Each client session will contain an appointment manager to
        store data related to the appointment that they are booking '''

    def __init__(self):
        self.store = None
        self.employee = None
        self.cal_month = None
        self.cal_year = None
        self.target_date = None
        self.target_time = None
        self.complete_reservation = None

    def _has_store(self):
        return bool(self.store)

    def _has_store_employee(self):
        return self._has_store() and bool(self.employee)

    def _has_store_employee_date(self):
        return self._has_store_employee() and bool(self.target_date)

    def _has_store_employee_date_time(self):
        return self._has_store_employee_date() and bool(self.target_time)

    def _has_complete_reservation(self):
        print(bool(self.complete_reservation))
        print(self.complete_reservation)
        return bool(self.complete_reservation)

    def ready_for_view(self, viewName):

        viewNames = {
                     'employee': self._has_store,
                     'calendar': self._has_store_employee,
                     'schedule': self._has_store_employee_date,
                     'appointment': self._has_store_employee_date_time,
                     'success': self._has_complete_reservation,
                     }

        return viewNames[viewName]()

    def has_valid_year_month(self): #used by for calendar navigation
        ''' checks if year and month are valid for creating calendar
            context '''
        valid_month = self.cal_month >= 1 and self.cal_month <= 12
        valid_year = self.cal_year <= 9998 and self.cal_year > 1
        return valid_month and valid_year

    def process_form(self, request, form):
        ''' process appointment form'''

        if self.target_time.is_booked == False:

            # Extract many-to-many objects and add to form if any exist
            if form.cleaned_data.has_key('services'):
                data = [x for x in form.cleaned_data['services']]

            # Prepare the form for the Reservation and add many-to-many objects.
            form = form.save(commit=False)

            # Mark the sessions timeblock as full
            tb = self.target_time
            print(tb)
            form.timeblock = tb
            print(form.timeblock)
            tb.is_booked = True
            tb.save()

            # Save the form and add many to many relationships
            form.save()
            if data:
                form.services.add(*data)

            # Add the reservation to the session
            request.session['apt_manager'].complete_reservation = form

        return form

    def send_confirmation_email(self, appointment):

        email_context = {}
        email_context['person'] = appointment.name
        email_context['phone_number'] = appointment.phone
        email_context['date'] = appointment.timeblock.__unicode__()
        email_context['services'] = appointment.services.all()
        email_context['customer_comment'] = appointment.customer_comment

        subject = "Shobiz: New Appointment"
        text = render_to_string('shobiz/confirm_reservation.txt', email_context)
        server_email = "shobiz.appointment@gmail.com"
        destination_email = ["mhinrichs@gmail.com",]
        send_mail(subject, text, server_email, destination_email, fail_silently = False)
