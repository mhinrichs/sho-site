from datetime import date
from calendar import Calendar
from shobiz.models import Employee, Customer, Store, Workday

class EmployeeWorkday:

    def __init__(self, store, employee, dateobject , status='grayed_out')
        self.store = store
        self.employee = employee
        self.date = dateobject
        self.status = status

class EmployeeCalendarMaker:

    def __init__(self, store, employee, weekdaystart = 6):
        self.calendar = Calendar(weekdaystart)
        self.store = store
        self.employee = employee

    def create_calendar(self):
        calendar = []
        for week in self.calendar:
            week = []
            for day in week:
                #todo process workdays

                week.append()
            calendar.append(week)
        return calendar




