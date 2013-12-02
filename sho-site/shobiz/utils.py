# -*- coding: utf-8 -*-

from datetime import date, datetime
from calendar import Calendar
from shobiz.models import Workday

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
        if not self.status: # None as status means no workday record / employee is off work
            self.status = 'offwork'

    def to_string(self):
        return self.date.strftime("%Y_%m_%d") #underscores because its used as an id in html tag

class WorkdayCalendar:

    '''Pairs workdays with calendar from the calendar module.
       The workdays are captured as a single query set to avoid hitting
       the database more than once.'''

    def __init__(self, weekdaystart = 6):
        self.calendar = Calendar(weekdaystart)

    def create_calendar(self, store, employee, year, month):
        ''' Gets a queryset containing workdays from the database.
            Pairs queryset with dates from the python calendar module
            and returns a new monthdatescalendar with the dates replaced
            with EmployeeWorkday objects.

            The status of the day (how many of the timeblocks are booked)
            is updated during the pairing process. '''
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

    def get_context(self, request):
        '''Gets an appropriate context for a calendar based off of
           a client sesssion'''
        context = {}
        context['days_of_week'] = self.get_weekdays()
        required_keys = ('store', 'employee')
        optional_keys = ('year', 'month')
        if all(request.session.has_key(key) for key in required_keys):
            if all(request.session.has_key(key) for key in optional_keys):
                context['year'] = request.session['year']
                context['month'] = request.session['month']
            else:
                d = datetime.now()
                context['year'] = d.year
                context['month'] = d.month
                request.session['year'] = d.year
                request.session['month'] = d.month
            year, month = context['year'], context['month']
            store, employee = request.session['store'], request.session['employee']
            context['store'] = store
            context['employee'] = employee
            context['calendar'] = self.create_calendar(store, employee, year, month)
        else:
            raise ValueError('insufficent data in request.session to get_calendar_context')
        return context




