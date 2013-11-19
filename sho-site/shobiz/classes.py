from datetime import date
from calendar import Calendar
from shobiz.models import Employee, Customer, Store, Workday

class EmployeeWorkday:

    def __init__(self, store, employee, dateobject, workday=None, status='grayed_out'):
        self.store = store
        self.employee = employee
        self.date = dateobject
        self.workday = workday
        self.status = status

    def pair_workday(self, query_set):
        for entry in query_set:
            if entry.date == self.date:
                print("matched")
                self.workday = entry
                self.status = entry.get_status()
                return self
            else:
                self.status = 'offwork'
        return self

class WorkdayCalendarMaker:
    '''this pairs workdays with calendar from the calendar module'''

    def __init__(self, weekdaystart = 6):
        self.calendar = Calendar(weekdaystart)

    def create_calendar(self, store_id, emp_id, year, month):
        query_set = Workday.by_store_emp_year_month(store_id, emp_id, year, month)
        print(query_set)
        calendar = []
        for week in self.calendar.monthdatescalendar(year, month):
            workweek = []
            for date in week:
                if date.month != month: #process status for other months (grayed)
                    workday = EmployeeWorkday(store_id, emp_id, date)
                else:  #process the date and match queries from the database
                    workday = EmployeeWorkday(store_id, emp_id, date).pair_workday(query_set)
                workweek.append(workday)
            calendar.append(workweek)
        return calendar
