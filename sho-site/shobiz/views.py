# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from shobiz.models import Store, Employee, Customer, Workday, TimeBlock
from shobiz.utils import WorkdayCalendar, AppointmentManager
from calendar import Calendar
from datetime import datetime

#for testing purposes



# Change after adding default Store and Employee to Database
USE_DEFAULT_STORE = False
USE_DEFAULT_EMPLOYEE = False
DEFAULT_STORE = '''default here'''
DEFAULT_EMPLOYEE = '''default employee'''

USE_DEFAULT_STORE = True
USE_DEFAULT_EMPLOYEE = True
DEFAULT_STORE = Store.objects.get(store_id = 's0001')
DEFAULT_EMPLOYEE = Employee.objects.get(emp_id = "e000001")


# WorkdayCalendar
WorkdayCalendar = WorkdayCalendar()

# Helper functions
def encode_datestr(datestring):
    ''' encodeds a datestr to a datetime object '''
    try:
        date = datetime.strptime(datestring, '%Y_%m_%d')
    except:
        raise ValueError("Must follow the format YYYY_M_D")
    return date

#views
def index(request):
    ''' The index page will start at store selection.
        This section can be skipped by adding the relevant
        default session data and moving on to a later step.'''
    context = {}
    request.session.flush()
    request.session['apt_manager'] = AppointmentManager()
    if USE_DEFAULT_STORE:
        request.session['apt_manager'].store = DEFAULT_STORE
        print("Currently set value for store {}".format(request.session['apt_manager'].store))
        return redirect(employee)
    elif request.method == 'GET': #write a view for selecting store
        return render(request, 'shobiz/index.html', context)
    else: # request.method == 'POST':
        pass

def employee(request):
    ''' Select an employee from a list of employees based
        off of the store that was selected '''
    print("Currently set value for store {} after redirect".format(request.session['apt_manager'].store))
    context = {}
    if not request.session.has_key('apt_manager') or \
       not request.session['apt_manager'].has_store():
        return redirect(index)
    if USE_DEFAULT_EMPLOYEE:
        print("Hello from the value of DEFAULT_EMPLOYEE {}".format(DEFAULT_EMPLOYEE))
        request.session['apt_manager'].employee = DEFAULT_EMPLOYEE
        request.session.modified = True
        print("Hello from the value set to DEFAULT_EMPLOYEE {}".format(request.session['apt_manager'].employee))
        return redirect(calendar)
    elif request.method == 'GET': #write a view for selecting employee
        return render(request, 'shobiz/employee.html', context)
    else: # request.method == 'POST':
        pass

def calendar(request):
    print(request.session.keys())
    print("@calendar store {}".format(request.session['apt_manager'].store))
    print("@calendar employee {}".format(request.session['apt_manager'].employee))
    if not request.session.has_key('apt_manager') or \
       not request.session['apt_manager'].has_store_employee():
        print(request.session.has_key('apt_manager'))
        print(request.session['apt_manager'].has_store_employee())
        print("looped at calendar")
        return redirect(index)
    d = datetime.now()
    request.session['apt_manager'].cal_year = d.year
    request.session['apt_manager'].cal_month = d.month
    context = WorkdayCalendar.get_calendar_context(request)
    return render(request, 'shobiz/calendar.html', context)

def calendar_ajax(request):
    try:
        request = WorkdayCalendar.navigate(request)
    except ValueError: #This only happens if someone trys to navigate past valid calandar values
        return redirect(index)
    context = WorkdayCalendar.get_calendar_context(request)
    return render(request, 'shobiz/calendar_template.html', context)

def schedule(request):
    try:
        if request.GET.has_key('date'):
            date = encode_datestr(request.GET['date'])
            request.session['date'] = date
        context = WorkdayCalendar.get_schedule_context(request)
    except ValueError:
        return redirect(index)
    return render(request, 'shobiz/schedule.html', context)

