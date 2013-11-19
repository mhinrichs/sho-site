from datetime import date
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
            if self.status == 'dimmed':
                pass
            elif entry.date == self.date:
                self.workday = entry
                self.status = entry.get_status()
        if not self.status:
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


