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

class WorkdayCalendarMaker:

    '''Pairs workdays with calendar from the calendar module.
       The workdays are captured as a single query set to avoid hitting
       the database more than once.'''

    def __init__(self, weekdaystart = 6):
        self.calendar = Calendar(weekdaystart)

    def get_calendar(self, store_id, emp_id, year, month):
        query_set = Workday.by_store_emp_year_month(store_id, emp_id, year, month)
        calendar = []
        for week in self.calendar.monthdatescalendar(year, month):
            workweek = []
            for date in week:
                if date.month != month: #process status for other months (dimmed)
                    workday = EmployeeWorkday(store_id, emp_id, date, None, 'dimmed')
                    workday.pair_workday(query_set)
                else:  #process the date and match queries from the database
                    workday = EmployeeWorkday(store_id, emp_id, date)
                    workday.pair_workday(query_set)
                workweek.append(workday)
            calendar.append(workweek)
        return calendar

    def get_weekdays(self):
        ''' todo optionally add weekdays for non japan regions '''
        return [r"日", r"月", r"火", r"水", r"木", r"金", r"土"]

    def get_context_with_calendar(self, request):
        context = {}
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
            context['store'] = request.session['store']
            context['employee'] = request.session['employee']
            context['days_of_week'] = self.get_weekdays()
            store_id, emp_id = context['store'].store_id, context['employee'].emp_id
            context['calendar'] = self.get_calendar(store_id, emp_id, year, month)
        else:
            raise ValueError('insufficent data in request.session to get_calendar_context')
        return context


