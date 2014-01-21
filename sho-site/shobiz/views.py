# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from shobiz.models import Store, Employee, Customer, Workday, TimeBlock
from shobiz.utils import WorkdayCalendar, AppointmentManager
from shobiz.forms import ReservationForm
from calendar import Calendar
from datetime import datetime

# WorkdayCalendar
WorkdayCalendar = WorkdayCalendar()

# Change after adding default Store and Employee to Database
USE_DEFAULT_STORE = True
USE_DEFAULT_EMPLOYEE = True
DEFAULT_STORE = Store.objects.get(store_id = 's0001')
DEFAULT_EMPLOYEE = Employee.objects.get(emp_id = 'e000001')

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
        request.session.modified = True
        return redirect(employee)
    elif request.method == 'GET': #write a view for selecting store
        return render(request, 'shobiz/index.html', context)
    else: # request.method == 'POST':
        pass

def employee(request):
    ''' Select an employee from a list of employees based
        off of the store that was selected '''
    context = {}
    if not request.session.has_key('apt_manager') or \
       not request.session['apt_manager'].has_store():
        return redirect(index)
    elif USE_DEFAULT_EMPLOYEE:
        request.session['apt_manager'].employee = DEFAULT_EMPLOYEE
        request.session.modified = True
        return redirect(calendar)
    elif request.method == 'GET': #write a view for selecting employee
        return render(request, 'shobiz/employee.html', context)
    else: # request.method == 'POST':
        pass

def calendar(request):
    if not request.session.has_key('apt_manager') or \
       not request.session['apt_manager'].has_store_employee():
        return redirect(index)
    else:
        d = datetime.now()
        request.session['apt_manager'].cal_year = d.year
        request.session['apt_manager'].cal_month = d.month
        request.session.modified = True
        context = WorkdayCalendar.get_calendar_context(request)
    return render(request, 'shobiz/calendar.html', context)

def calendar_ajax(request):
    try:
        WorkdayCalendar.navigate(request)
        request.session.modified = True
    except ValueError: #This only happens if someone trys to navigate past valid calandar values
        return redirect(index)
    context = WorkdayCalendar.get_calendar_context(request)
    return render(request, 'shobiz/calendar_template.html', context)

def schedule(request):
    if not request.session.has_key('apt_manager') or \
       not request.session['apt_manager'].has_store_employee():
        return redirect(index)
    elif request.GET.has_key('date'):
        date = encode_datestr(request.GET['date'])
        request.session['apt_manager'].target_date = date
        request.session.modified = True
    else:
        pass
    context = WorkdayCalendar.get_schedule_context(request)
    return render(request, 'shobiz/schedule.html', context)


def make_appointment(request):
    if not request.session.has_key('apt_manager') or \
       not request.session['apt_manager'].has_store_employee_date():
        return redirect(index)
    else:
        if request.method == 'POST':
            form = ReservationForm(request.POST)
            if form.is_valid():
                form.save(commit=True)
                return success(request)
            else:
                print(form.errors)
        else:
            form = ReservationForm()
    context = {'form': form}
    return render(request, 'shobiz/appointment.html', context)

def success(request):
    '''When customer confirms appointment sends confirmation mail to manager.'''
    pass
